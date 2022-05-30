import datetime
import os
import subprocess
import json



class ChangeLogGenerator:
    def __init__(self, property_obj, version_obj, change_log_content_obj):
        self.property_obj = property_obj
        self.version_obj = version_obj
        self.change_log_content_obj = change_log_content_obj
        self.properties = property_obj.get_properties()

    def generate_changelog_entry(self):

        changelog_version = self.version_obj.version
        changelog_description = self.change_log_content_obj.changelog_entry

        # In case changelog message is empty then there is no need to bump changelog .....
        if changelog_description:
            # Get the date to be bump into ChangeLog.md file
            date = datetime.datetime.now().strftime(self.properties['dateFormat'])
            # Now replace version , date and changelog in the template of changelog so to get an entry to committed in
            # ßChangelog.md file.
            change_log_entry = self.get_changelog_template().replace("$version", changelog_version).replace("$date", date).replace("$changelog", changelog_description)
            # Check if CHANGELOG.md file is present or not
            self.check_file_existence()

            # Now add the changelog entry to first line of Changelog.md file..
            self.prepend_change_log_entry_to_change_log_file(change_log_entry)
            self.push_change_log_file()
        else:
            print("Changelog entry is not present in the commit message")

    @staticmethod
    def get_changelog_template():
        return "## $version ($date) \n $changelog \n"

    # This function will check whether the file is present or not.
    # If the file is not present then it will create the file

    def check_file_existence(self):
        changelog_file_name = self.properties['changelogFileName']
        if not os.path.exists(changelog_file_name):
            fp = open(changelog_file_name, 'x')
            fp.close()

    # This function will dynamically build the repository path.

    def get_repository_path(self):
        repo_path = ""
        repo_path = repo_path + "https://" + self.properties['gitlab_username'] + ":" + self.properties['gitlab_token'] + "@" + self.properties['ci_server_host'] + "/" + self.properties['ci_project_path'] + ".git"
        return repo_path

    # This function will be used to prepend the changelog text in the changelog.md file.

    def prepend_change_log_entry_to_change_log_file(self, change_log_entry):
        changelog_file_name = self.properties['changelogFileName']
        with open(changelog_file_name, 'r') as f:
            existing_content = f.read()
        change_log_content = change_log_entry + existing_content
        f.close()

        with open(changelog_file_name, 'w') as f:
            f.write(change_log_content)
        f.close()

    def push_change_log_file(self):
        gitlab_user_email = self.properties['gitUserEmail']
        changelog_file_name = self.properties['changelogFileName']
        changelog_commit_message = self.properties['changelogCommitMessage']
        changelog_commit_branch = self.properties['ci_commit_branch']
        commit_sha = self.properties['ci_commit_sha']

        subprocess.run(['git', 'config', '--global', 'user.email', gitlab_user_email])
        subprocess.run(['git', 'add', changelog_file_name])
        subprocess.run(['git', 'commit', '-m', changelog_commit_message])

        try:
            subprocess.run(['git', 'push', 'origin', changelog_commit_branch, '-o', 'ci.skip'], check=True)
        except Exception as ex:
            print("Exception occurred while pushing")
            os.chdir("..")
            subprocess.run(['rm', '-r', commit_sha])
            # generate_change_log()


class Property:

    def __init__(self, properties_file_path):
        properties_file = open(properties_file_path)
        # returns JSON object as a dictionary
        properties = json.load(properties_file)
        # Closing file
        properties_file.close()
        properties['gitlab_username'] = os.environ.get("GITLAB_USERNAME")
        properties['gitlab_token'] = os.environ.get("GITLAB_TOKEN")
        properties['ci_server_host'] = os.environ.get("CI_SERVER_HOST")
        properties['ci_project_path'] = os.environ.get("CI_PROJECT_PATH")
        properties['ci_commit_sha'] = os.environ.get("CI_COMMIT_SHA")
        properties['ci_commit_short_sha'] = os.environ.get("CI_COMMIT_SHORT_SHA")
        properties['version'] = os.environ.get("VERSION")
        properties['ci_commit_branch'] = os.environ.get("CI_COMMIT_BRANCH")
        properties['commit_message_description'] = os.environ.get("CI_COMMIT_DESCRIPTION")
        self.properties = properties

    def get_properties(self):

        return self.properties


class Version:
    def __init__(self, property_obj):
        properties = property_obj.get_properties()
        commit_count = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], stdout= subprocess.PIPE)
        commit_count = str(commit_count.stdout.decode('utf-8'))
        print(commit_count)
        self.version = properties['version'] + "-" + commit_count.strip() + "-" + properties['ci_commit_short_sha']


class ChangeLogContent:

    def __init__(self, property_obj):
        properties = property_obj.get_properties()
        if properties['changelogIdentifier'] in properties['commit_message_description']:
            self.changelog_entry = properties['commit_message_description'].partition( properties['changelogIdentifier'])[2]
        else:
            self.changelog_entry = ""


def populate_changelog():

    properties_obj = Property('changeLogGenerator.json')
    changelog_content_obj = ChangeLogContent(properties_obj)
    repository_path = "https://" + properties_obj.properties['gitlab_username'] + ":" + properties_obj.properties['gitlab_token'] + "@" + properties_obj.properties['ci_server_host'] + "/" + properties_obj.properties['ci_project_path'] + ".git"
    # using repo path clone the repo in a folder whose name will be the commit_SHA.
    os.system("git clone --single-branch --branch " + properties_obj.properties['ci_commit_branch'] + " " + repository_path + " " + properties_obj.properties['ci_commit_sha'])
    # change the working directory to a folder in which repo has been cloned.
    os.chdir(properties_obj.properties['ci_commit_sha'])
    version_obj = Version(properties_obj)
    ChangeLogGenerator(properties_obj, version_obj, changelog_content_obj).generate_changelog_entry()


