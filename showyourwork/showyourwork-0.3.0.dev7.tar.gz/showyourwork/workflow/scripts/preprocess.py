r"""
Does a first pass through the manuscript to infer the workflow graph.

This does a fast compile of the article, overriding commands like
``\label``, ``\script``, ``\variable``, and 
``\includegraphics`` to instead print their arguments to an XML
log file, which we use to infer the relationships between input and output
files. This information is then used to build the workflow graph for the
main article build step.

"""
from showyourwork import paths, exceptions, zenodo
from showyourwork.zenodo import Zenodo
from showyourwork.tex import compile_tex
import sys
import json
import re
from pathlib import Path
from collections.abc import MutableMapping
from xml.etree.ElementTree import parse as ParseXMLTree


def flatten_dataset_contents(d, parent_key="", default_path=None):
    """
    Flatten the ``contents`` dictionary of a dataset entry, filling
    in default mappings and removing zipfile extensions from the target path.
    Adapted from `<https://stackoverflow.com/a/6027615>`_.

    Args:
        d (dict): The dataset ``contents`` dictionary.
        parent_key (str): The parent key of the current dictionary.
        default_path (str, optional): The default path to use if the target is not specified.

    """
    if not default_path:
        default_path = paths.user().data.relative_to(paths.user().repo)
    items = []
    if type(d) is str:
        d = {d: None}
    elif type(d) is list:
        raise exceptions.ConfigError(
            "Error parsing the config. "
            "Something is not formatted correctly in the `datasets` field."
        )

    for k, v in d.items():
        new_key = (Path(parent_key) / k).as_posix() if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(
                flatten_dataset_contents(
                    v, new_key, default_path=default_path
                ).items()
            )
        else:
            if v is None:
                # Use the default path
                # If inside a zipfile, remove the zipfile extension
                # from the target path
                zip_file = Path(new_key).parts[0]
                for ext in zenodo.zip_exts:
                    if len(Path(new_key).parts) > 1 and zip_file.endswith(
                        f".{ext}"
                    ):
                        mod_key = Path(new_key).parts[0][
                            : -len(f".{ext}")
                        ] / Path(*Path(new_key).parts[1:])
                        v = (Path(default_path) / mod_key).as_posix()
                        break
                else:
                    v = (Path(default_path) / new_key).as_posix()
            items.append((new_key, v))
    return dict(items)


def parse_datasets():
    """
    Parse the ``datasets`` keys in the config file and populate entries with
    custom metadata.

    """

    for doi, entry in config["datasets"].items():

        # Parse the DOI to get the Zenodo ID
        deposit = Zenodo(doi)

        # Require that this is a static *version* ID
        entry["id_type"] = deposit.get_id_type()
        if entry["id_type"] != "version":
            if entry["id_type"] == "concept":
                raise exceptions.InvalidZenodoIdType(
                    "Error parsing the config. "
                    f"{doi} seems to be a concept DOI."
                    "Datasets should be specified using their static "
                    "version DOI instead."
                )
            else:
                raise exceptions.InvalidZenodoIdType(
                    "Error parsing the config. "
                    f"{doi} is not a valid version DOI."
                )

        # Deposit contents
        entry["destination"] = entry.get(
            "destination",
            str(paths.user().data.relative_to(paths.user().repo)),
        )
        contents = flatten_dataset_contents(
            entry.get("contents", {}), default_path=entry["destination"]
        )

        # Handle files inside zipfiles, tarballs, etc.
        entry["zip_files"] = {}
        tmp_path = deposit.path().relative_to(paths.user().repo)
        for source in list(contents.keys()):

            # Ensure the target is not a list
            target = contents[source]
            if type(target) is list:
                raise exceptions.ZenodoContentsError(
                    "Error parsing the config. "
                    "The `contents` field of a Zenodo deposit must be "
                    "provided as a mapping, not as a list."
                )

            # If it's a file inside a zipfile, add it to a separate entry in the config
            zip_file = Path(source).parts[0]
            if len(Path(source).parts) > 1 and any(
                [zip_file.endswith(f".{ext}") for ext in zenodo.zip_exts]
            ):
                new_source = Path(*Path(source).parts[1:]).as_posix()
                if zip_file in entry["zip_files"].keys():
                    entry["zip_files"][zip_file].update({new_source: target})
                else:
                    entry["zip_files"][zip_file] = {new_source: target}

                # Remove it from the `contents` entry
                del contents[source]

                # We'll store the zipfile in a temporary directory
                contents[zip_file] = (
                    tmp_path / str(deposit.deposit_id) / zip_file
                ).as_posix()

        entry["contents"] = contents


def check_figure_format(figure):
    """
    Check that all figures are declared correctly in `tex/ms.tex`
    so we can parse them corresponding XML tree.

    Args:
        figure: A figure XML element.
    """
    # Get all figure elements
    elements = list(figure)
    captions = figure.findall("CAPTION")
    labels = figure.findall("LABEL")
    scripts = figure.findall("SCRIPT")

    # Check that figure labels aren't nested inside captions
    for caption in captions:
        caption_labels = caption.findall("LABEL")
        if len(caption_labels):
            raise exceptions.FigureFormatError(
                "Label `{}` should not be nested within the figure caption".format(
                    caption_labels[0].text
                )
            )

    # The label must always come after the figure caption
    # Any marginicons must always come before the label
    if len(captions):

        # Index of last caption
        for caption_idx, element in enumerate(elements[::-1]):
            if element.tag == "CAPTION":
                break
        caption_idx = len(elements) - 1 - caption_idx

        if len(labels):

            # Index of first label
            for label_idx, element in enumerate(elements):
                if element.tag == "LABEL":
                    break

            if label_idx < caption_idx:
                raise exceptions.FigureFormatError(
                    "Figure label `{}` must come after the caption.".format(
                        (labels)[0].text
                    )
                )

            # Index of last marginicon
            for marginicon_idx, element in enumerate(elements):
                if element.tag == "MARGINICON":
                    break
            else:
                marginicon_idx = 0

            if marginicon_idx > label_idx:
                raise exceptions.FigureFormatError(
                    "Command \marginicon must always come before the figure label."
                )

    # Check that there is at most one label
    if len(labels) >= 2:
        raise exceptions.FigureFormatError(
            "A figure has multiple labels: `{}`".format(
                ", ".join(label.text for label in labels)
            )
        )

    # Check that there is at most one script
    if len(scripts) >= 2:
        raise exceptions.FigureFormatError(
            "A figure has multiple scripts: `{}`".format(
                ", ".join(script.text for script in scripts)
            )
        )

    # If there's a script, there must be a label
    if len(scripts) and not len(labels):
        raise exceptions.FigureFormatError(
            "A figure defines a script but has no label: `{}`".format(
                ", ".join(script.text for script in scripts)
            )
        )


def get_xml_tree():
    """Compiles the TeX file to generate the XML tree.

    Returns:
        xml.etree.ElementTree.ElementTree: The XML tree.
    """

    # Parameters
    xmlfile = paths.user().preprocess / "showyourwork.xml"

    # Build the paper to get the XML file
    compile_tex(
        config,
        args=[
            "-r",
            "0",
        ],
        output_dir=paths.user().preprocess,
        stylesheet=paths.showyourwork().resources
        / "styles"
        / "preprocess.tex",
    )

    # Add <HTML></HTML> tags to the XML file
    if xmlfile.exists():
        with open(xmlfile, "r") as f:
            contents = f.read()
    else:
        raise exceptions.MissingXMLFile(
            r"Article parsing failed. Did you forget to `\usepackage{showyourwork}`?"
        )

    contents = "<HTML>\n" + contents + "</HTML>"
    with open(xmlfile, "w") as f:
        print(contents, file=f)

    # Load the XML tree
    return ParseXMLTree(paths.user().preprocess / "showyourwork.xml").getroot()


def get_json_tree():
    """Builds a dictionary containing mappings between input and output files.
    
    Returns:
        dict: The JSON dependency tree for the article.
    """
    # Get the XML article tree
    xml_tree = get_xml_tree()

    # Parse the \graphicspath command
    # Note that if there are multiple graphicspath calls, only the first one
    # is read. Same for multiple directories within a graphicspath call.
    try:
        graphicspath = xml_tree.findall("GRAPHICSPATH")
        if len(graphicspath) == 0:
            graphicspath = Path(".")
        else:
            graphicspath = re.findall("\{(.*?)\}", graphicspath[-1].text)[0]
            graphicspath = Path(graphicspath)
    except:
        raise exceptions.GraphicsPathError()

    # Parse labeled graphics inside `figure` environments
    figures = {}
    unlabeled_graphics = []
    for figure in xml_tree.findall("FIGURE"):

        # Ensure the figure environment conforms to the standard
        check_figure_format(figure)

        # Find all graphics included in this figure environment
        graphics = [
            str(
                (paths.user().tex / graphicspath / graphic.text)
                .resolve()
                .relative_to(paths.user().repo)
            )
            for graphic in figure.findall("GRAPHICS")
        ]

        # Are these static figures?
        static = all(
            [
                (paths.user().repo / graphic).parents[0]
                == paths.user().figures
                and (paths.user().static / Path(graphic).name).exists()
                for graphic in graphics
            ]
        )

        # Get the figure \label, if it exists
        labels = figure.findall("LABEL")
        if len(labels):

            # We already checked that there's only one label above
            label = labels[0].text

        else:

            # Treat these as free-floating graphics
            unlabeled_graphics.extend(graphics)
            continue

        # Get the figure \script, if it exists
        scripts = figure.findall("SCRIPT")
        if len(scripts) and scripts[0].text is not None:

            # The user provided an argument to \script{}, which we assume
            # is the name of the script relative to the figure scripts
            # directory
            script = str(
                (paths.user().scripts / scripts[0].text).relative_to(
                    paths.user().repo
                )
            )

            # Infer the command we'll use to execute the script based on its
            # extension. Assume the extension is the string following the
            # last '.' in the script name; if that's not a known extension,
            # proceed leftward until we find a match (covers cases like
            # *.tar.gz, etc.)
            parts = scripts[0].text.split(".")
            for i in range(1, len(parts)):
                ext = ".".join(parts[-i:])
                if ext in config["script_extensions"]:
                    command = config["scripts"][ext]
                    break
            else:
                raise exceptions.FigureGenerationError(
                    "Can't determine how to execute the figure "
                    f"script {scripts[0].text}. Please provide instructions "
                    "on how to execute scripts with this extension in the "
                    "config file."
                )

        else:

            # No script provided
            script = None

            # If all the figures in this environment exist in the
            # static directory, set up the command to copy them over
            if static:
                srcs = " ".join(
                    [
                        str(
                            (
                                paths.user().static / Path(graphic).name
                            ).relative_to(paths.user().repo)
                        )
                        for graphic in graphics
                    ]
                )
                dest = paths.user().figures.relative_to(paths.user().repo)
                command = f"cp {srcs} {dest}"

            else:

                # We don't know how to generate this figure at this time.
                # Hopefully the user specified a custom Snakemake rule!
                command = None

        # Collect user-defined dependencies
        dependencies = config["dependencies"].get(script, [])

        # If any of the dependencies exists in a Zenodo deposit, infer
        # its URL here so we can add margin links to the PDF
        datasets = []
        for doi in config["datasets"]:
            deposit = Zenodo(doi)
            url = f"https://{deposit.url}/record/{deposit.deposit_id}"
            for dep in dependencies:
                if dep in config["datasets"][doi]["contents"].values():
                    datasets.append(url)
                else:
                    for zip_file in config["datasets"][doi]["zip_files"]:
                        if (
                            dep
                            in config["datasets"][doi]["zip_files"][
                                zip_file
                            ].values()
                        ):
                            datasets.append(url)
                            break
        datasets = list(set(datasets))

        # Format the command by replacing placeholders
        if command is not None:
            command = command.format(
                script=script,
                output=" ".join(graphics),
                datasets=" ".join(datasets),
                dependencies=" ".join(dependencies),
            )

        # Add an entry to the tree
        figures[label] = {
            "script": script,
            "graphics": graphics,
            "datasets": datasets,
            "dependencies": dependencies,
            "command": command,
        }

    # Parse free-floating graphics
    free_floating_graphics = [
        str(
            (paths.user().tex / graphicspath / graphic.text)
            .resolve()
            .relative_to(paths.user().repo)
        )
        for graphic in xml_tree.findall("GRAPHICS")
    ] + unlabeled_graphics

    # Ignore graphics that are dependencies of the texfile (such as orcid-ID.png)
    free_floating_graphics = [
        graphic
        for graphic in free_floating_graphics
        if graphic not in config["tex_files_out"]
    ]

    # Separate into dynamic and static figures
    free_floating_static = [
        graphic
        for graphic in free_floating_graphics
        if (paths.user().repo / graphic).parents[0] == paths.user().figures
        and (paths.user().static / Path(graphic).name).exists()
    ]
    free_floating_dynamic = [
        graphic
        for graphic in free_floating_graphics
        if graphic not in free_floating_static
    ]

    # Add entries to the tree: dynamic figures
    # (User should provide a custom Snakemake rule)
    figures["free-floating-dynamic"] = {
        "script": None,
        "graphics": free_floating_dynamic,
        "datasets": [],
        "dependencies": [],
        "command": None,
    }

    # Add entries to the tree: static figures
    # (copy them over from the static folder)
    srcs = " ".join(
        [
            str(
                (paths.user().static / Path(graphic).name).relative_to(
                    paths.user().repo
                )
            )
            for graphic in free_floating_static
        ]
    )
    dest = paths.user().figures.relative_to(paths.user().repo)
    figures["free-floating-static"] = {
        "script": None,
        "graphics": free_floating_static,
        "datasets": [],
        "dependencies": [],
        "command": f"cp {srcs} {dest}",
    }

    # Parse files included using the \input statement;
    # these will be made explicit dependencies of the build
    files = [
        str(
            (paths.user().tex / file.text)
            .resolve()
            .relative_to(paths.user().repo)
        )
        for file in xml_tree.findall("INPUT")
    ]

    # The full tree (someday we'll have equations in here, too)
    tree = {"figures": figures, "files": files}

    return tree


if __name__ == "__main__":

    # Snakemake config (available automagically)
    config = snakemake.config  # type:ignore

    # Parse the `datasets` key in the config
    parse_datasets()

    # Get the article tree
    config["tree"] = get_json_tree()

    # Make all of the graphics dependencies of the article
    config["dependencies"][config["ms_tex"]] = config["dependencies"].get(
        config["ms_tex"], []
    )
    for figure_name in config["tree"]["figures"]:
        graphics = config["tree"]["figures"][figure_name]["graphics"]
        config["dependencies"][config["ms_tex"]].extend(
            [Path(graphic).as_posix() for graphic in graphics]
        )

    # Make files specified as \variable dependencies of the article
    config["dependencies"][config["ms_tex"]].extend(
        [Path(file).as_posix() for file in config["tree"]["files"]]
    )

    # Gather the figure script & dataset info so we can access it on the TeX side
    config["labels"] = {}
    for label, value in config["tree"]["figures"].items():
        script = value["script"]
        if script is not None:
            config["labels"][f"{label}_script"] = script
        datasets = value["datasets"]
        # Note: built-in max of 3 datasets will be displayed
        for dataset, number in zip(datasets, ["One", "Two", "Three"]):
            config["labels"][f"{label}_dataset{number}"] = dataset

    # Save the config file
    with open(config["config_json"], "w") as f:
        print(json.dumps(config, indent=4), file=f)