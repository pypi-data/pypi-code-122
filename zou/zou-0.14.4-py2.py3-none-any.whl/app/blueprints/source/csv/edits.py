from zou.app.blueprints.source.csv.base import BaseCsvProjectImportResource
from zou.app.models.project import ProjectTaskTypeLink
from zou.app.models.task_type import TaskType

from zou.app.services import edits_service, projects_service, shots_service
from zou.app.models.entity import Entity
from zou.app.services.tasks_service import (
    create_task,
    create_tasks,
    get_tasks_for_edit,
    get_task_statuses,
)
from zou.app.services.comments_service import create_comment
from zou.app.services.persons_service import get_current_user
from zou.app.services.exception import TaskStatusNotFoundException
from zou.app.utils import events


class EditsCsvImportResource(BaseCsvProjectImportResource):
    def prepare_import(self, project_id):
        self.episodes = {}
        self.entity_types = {}
        self.descriptor_fields = self.get_descriptor_field_map(
            project_id, "Edit"
        )
        project = projects_service.get_project(project_id)
        self.is_tv_show = projects_service.is_tv_show(project)
        if self.is_tv_show:
            episodes = shots_service.get_episodes_for_project(project_id)
            self.episodes = {
                episode["name"]: episode["id"] for episode in episodes
            }
        self.created_edits = []
        self.task_types_in_project_for_edits = (
            TaskType.query.join(ProjectTaskTypeLink)
            .filter(ProjectTaskTypeLink.project_id == project_id)
            .filter(TaskType.for_entity == "Edit")
        )
        self.task_statuses = {
            status["id"]: [status[n].lower() for n in ("name", "short_name")]
            for status in get_task_statuses()
        }
        self.current_user_id = get_current_user()["id"]

    def import_row(self, row, project_id):
        asset_name = row["Name"]
        description = row.get("Description", "")
        episode_name = row.get("Episode", None)
        episode_id = None
        if episode_name is not None:
            if episode_name not in self.episodes:
                self.episodes[
                    episode_name
                ] = shots_service.get_or_create_episode(
                    project_id, episode_name
                )[
                    "id"
                ]
            episode_id = self.episodes.get(episode_name, None)

        edit_type_id = edits_service.get_edit_type()["id"]
        entity = Entity.get_by(
            name=asset_name,
            project_id=project_id,
            entity_type_id=edit_type_id,
            source_id=episode_id,
        )

        data = {}
        for name, field_name in self.descriptor_fields.items():
            if name in row:
                data[field_name] = row[name]
            elif (
                entity is not None
                and entity.data is not None
                and field_name in entity.data
            ):
                data[field_name] = entity.data[field_name]

        # Search for task name and comment column and append values to update
        # in a dictionnary using task name as key.
        tasks_update = {}
        for task_type in self.task_types_in_project_for_edits:
            # search for status update and get this id if found
            task_status_name = row.get(task_type.name.title(), "").lower()
            task_status_id = ""
            if task_status_name:
                for status_id, status_names in self.task_statuses.items():
                    if task_status_name in status_names:
                        task_status_id = status_id
                        break
                else:
                    raise TaskStatusNotFoundException(
                        "Task status not found for %s" % task_status_name
                    )
            # search for comment
            task_comment_text = row.get(
                "%s comment" % task_type.name.title(), ""
            )
            # append updates if valided
            if task_status_id or task_comment_text:
                tasks_update[task_type.name] = {
                    "status": task_status_id,
                    "comment": task_comment_text,
                }

        tasks = []
        if entity is None:
            entity = Entity.create(
                name=asset_name,
                description=description,
                project_id=project_id,
                entity_type_id=edit_type_id,
                source_id=episode_id,
                data=data,
            )
            events.emit(
                "edit:new",
                {"edit_id": str(entity.id), "episode_id": episode_id},
                project_id=project_id,
            )
            if tasks_update:
                # if task updates are required we need to create entity tasks
                # imediatly and update this at the end of current row import
                # process.
                for task_type in self.task_types_in_project_for_edits:
                    tasks.append(
                        create_task(task_type.serialize(), entity.serialize())
                    )
            else:
                # if there is no update for task we append the entity in the
                # created entities list in order to optimize task creation in
                # the run_import method call when all rows are imported.
                self.created_edits.append(entity.serialize())

        elif self.is_update:
            entity.update({"description": description, "data": data})
            events.emit(
                "edit:update",
                {"edit_id": str(entity.id), "episode_id": episode_id},
                project_id=project_id,
            )
            if tasks_update:
                tasks = get_tasks_for_edit(str(entity.id))

        # Update task status and/or comment using the created tasks list and
        # the tasks_update dictionnary.
        for task in tasks:
            task_name = task["task_type_name"]
            if task_name in tasks_update:
                task_status = tasks_update[task_name]["status"]
                task_comment = tasks_update[task_name]["comment"]
                if task_status != task["task_status_id"] or task_comment:
                    create_comment(
                        self.current_user_id,
                        task["id"],
                        task_status or task["task_status_id"],
                        task_comment,
                        [],
                        {},
                        "",
                    )

        return entity.serialize()

    def run_import(self, project_id, file_path):
        entities = super().run_import(project_id, file_path)
        for task_type in self.task_types_in_project_for_edits:
            create_tasks(task_type.serialize(), self.created_edits)
        return entities
