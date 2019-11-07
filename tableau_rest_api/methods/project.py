from .rest_api_base import *
class ProjectMethods(TableauRestApiBase):
    #
    # Start Project Querying methods
    #

    def query_projects(self) -> etree.Element:
        self.start_log_block()
        projects = self.query_resource("projects")
        self.end_log_block()
        return projects

    def query_projects_json(self, page_number: Optional[int] = None) -> str:
        self.start_log_block()
        projects = self.query_resource_json("projects", page_number=page_number)
        self.end_log_block()
        return projects

    def create_project(self, project_name: Optional[str] = None, project_desc: Optional[str] = None,
                       locked_permissions: bool = True, publish_samples: bool = False,
                       no_return: Optional[bool] = False,
                       direct_xml_request: Optional[etree.Element] = None) -> Project21:
        self.start_log_block()
        if direct_xml_request is not None:
            tsr = direct_xml_request
        else:
            tsr = etree.Element("tsRequest")
            p = etree.Element("project")
            p.set("name", project_name)

            if project_desc is not None:
                p.set('description', project_desc)
            if locked_permissions is not False:
                p.set('contentPermissions', "LockedToProject")
            tsr.append(p)

        url = self.build_api_url("projects")
        if publish_samples is True:
            url += '?publishSamples=true'
        try:
            new_project = self.send_add_request(url, tsr)
            self.end_log_block()
            project_luid = new_project.findall('.//t:project', self.ns_map)[0].get("id")
            if no_return is False:
                return self.get_published_project_object(project_luid, new_project)
        except RecoverableHTTPException as e:
            if e.http_code == 409:
                self.log('Project named {} already exists, finding and returning the Published Project Object'.format(
                    project_name))
                self.end_log_block()
                if no_return is False:
                    return self.get_published_project_object(project_name_or_luid=project_name)

    def query_project_luid(self, project_name: str) -> str:
        self.start_log_block()
        project_luid = self.query_luid_from_name(content_type='project', name=project_name)
        self.end_log_block()
        return project_luid

    def query_project_xml_object(self, project_name_or_luid: str) -> etree.Element:
        self.start_log_block()
        luid = self.query_project_luid(project_name_or_luid)
        proj_xml = self.query_single_element_from_endpoint('project', luid)
        self.end_log_block()
        return proj_xml

    def create_project(self, project_name=None, project_desc=None, locked_permissions=True, no_return=False,
                       direct_xml_request=None):
        """
        :type project_name: unicode
        :type project_desc: unicode
        :type locked_permissions: bool
        :type no_return: bool
        :type direct_xml_request: etree.Element
        :rtype: Project21
        """
        self.start_log_block()
        if direct_xml_request is not None:
            tsr = direct_xml_request
        else:
            tsr = etree.Element("tsRequest")
            p = etree.Element("project")
            p.set("name", project_name)

            if project_desc is not None:
                p.set('description', project_desc)
            if locked_permissions is not False:
                p.set('contentPermissions', "LockedToProject")
            tsr.append(p)

        url = self.build_api_url("projects")
        try:
            new_project = self.send_add_request(url, tsr)
            self.end_log_block()
            project_luid = new_project.findall('.//t:project', self.ns_map)[0].get("id")
            if no_return is False:
                return self.get_published_project_object(project_luid, new_project)
        except RecoverableHTTPException as e:
            if e.http_code == 409:
                self.log('Project named {} already exists, finding and returning the Published Project Object'.format(
                    project_name))
                self.end_log_block()
                if no_return is False:
                    return self.get_published_project_object(project_name_or_luid=project_name)

    #
    # End Project Querying Methods
    #