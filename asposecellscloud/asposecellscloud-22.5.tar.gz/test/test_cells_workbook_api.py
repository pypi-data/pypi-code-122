# coding: utf-8

"""
    Web API Swagger specification

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest
import warnings

ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)) + "/..")
sys.path.append(ABSPATH)
import asposecellscloud
from asposecellscloud.rest import ApiException
from asposecellscloud.apis.cells_api import CellsApi
import AuthUtil
from asposecellscloud.models import WorkbookEncryptionRequest
from asposecellscloud.models import WorkbookProtectionRequest
from asposecellscloud.models import ImportIntArrayOption
from asposecellscloud.models import CalculationOptions
from asposecellscloud.models import WorkbookSettings
from asposecellscloud.models import PasswordRequest
from datetime import datetime
global_api = None

class TestCellsWorkbookApi(unittest.TestCase):
    """ CellsWorkbookApi unit test stubs """

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        global global_api
        if global_api is None:
           global_api = asposecellscloud.apis.cells_api.CellsApi(AuthUtil.GetClientId(),AuthUtil.GetClientSecret(),"v3.0",AuthUtil.GetBaseUrl())
        self.api = global_api

    def tearDown(self):
        pass

    def test_cells_workbook_delete_decrypt_document(self):
        """
        Test case for cells_workbook_delete_decrypt_document

        Decrypt document.
        """
        name ='Book1.xlsx'  
        encryption = WorkbookEncryptionRequest(key_length = 128)
        encryption.password = "123456"
        encryption.encryption_type = "XOR"
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_delete_decrypt_document(name, encryption=encryption,folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_delete_document_unprotect_from_changes(self):
        """
        Test case for cells_workbook_delete_document_unprotect_from_changes

        Unprotect document from changes.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_delete_document_unprotect_from_changes(name, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_delete_unprotect_document(self):
        """
        Test case for cells_workbook_delete_unprotect_document

        Unprotect document.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        protection = WorkbookProtectionRequest()
        protection.password = "123"
        protection.protection_type = "All"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_delete_unprotect_document(name, protection=protection, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_delete_workbook_name(self):
        """
        Test case for cells_workbook_delete_workbook_name

        Clean workbook's names.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        name_name = "Name_2"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_delete_workbook_name(name, name_name, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_delete_workbook_names(self):
        """
        Test case for cells_workbook_delete_workbook_names

        Clean workbook's names.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_delete_workbook_names(name, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_get_workbook(self):
        """
        Test case for cells_workbook_get_workbook

        Read workbook info or export.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        password = None
        isAutoFit = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook(name,password=password,is_auto_fit=isAutoFit, folder=folder)
        # self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_get_workbook_format(self):
        """
        Test case for cells_workbook_get_workbook with format

        Read workbook info or export.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        password = None
        isAutoFit = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook(name,password=password,format="xlsx", is_auto_fit=isAutoFit, folder=folder)
        # self.assertEqual(result.code,200)
        pass
    def test_cells_workbook_get_workbook_extend(self):
        """
        Test case for cells_workbook_get_workbook with format

        Read workbook info or export.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        password = None
        isAutoFit = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook(name,password=password,format="pdf", is_auto_fit=isAutoFit, folder=folder, extended_query_parameters ={"OnePagePerSheet":"false"})
        # self.assertEqual(result.code,200)
        pass    
    def test_cells_workbook_get_workbook_JSON(self):
        """
        Test case for cells_workbook_get_workbook with format

        Read workbook info or export.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        password = None
        isAutoFit = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook(name,password=password,format="json", is_auto_fit=isAutoFit, folder=folder)
        # self.assertEqual(result.code,200)
        pass
    def test_cells_workbook_get_workbook_format_to_other_storage(self):
        """
        Test case for cells_workbook_get_workbook with format

        Read workbook info or export.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        password = None
        isAutoFit = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook(name,password=password,format="pdf", is_auto_fit=isAutoFit, folder=folder , out_path="Freeing/Workbook1_python.pdf",  out_storage_name="DropBox")
        # self.assertEqual(result.code,200)
        pass    
    def test_cells_workbook_get_workbook_format_md(self):
        """
        Test case for cells_workbook_get_workbook with format

        Read workbook info or export.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        password = None
        isAutoFit = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook(name,password=password,format="md", is_auto_fit=isAutoFit, folder=folder)
        # self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_get_workbook_default_style(self):
        """
        Test case for cells_workbook_get_workbook_default_style

        Read workbook default style info.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook_default_style(name, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_get_workbook_name(self):
        """
        Test case for cells_workbook_get_workbook_name

        Read workbook's name.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        nameName = "Name_2"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook_name(name, nameName, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_get_workbook_name_value(self):
        """
        Test case for cells_workbook_get_workbook_name_value

        Get workbook's name value.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        name_name = "Name_2"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook_name_value(name, name_name, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_get_workbook_names(self):
        """
        Test case for cells_workbook_get_workbook_names

        Read workbook's names.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook_names(name, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_get_workbook_text_items(self):
        """
        Test case for cells_workbook_get_workbook_text_items

        Read workbook's text items.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook_text_items(name, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_get_workbook_settings(self):
        """
        Test case for cells_workbook_get_workbook_settings

        Get Workbook Settings DTO
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_workbook_settings(name, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_autofit_workbook_rows(self):
        """
        Test case for cells_workbook_post_autofit_workbook_rows

        Autofit workbook rows.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        autoFitterOptions = None
        startRow = 1
        endRow = 100
        onlyAuto = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_autofit_workbook_rows(name, auto_fitter_options=autoFitterOptions, start_row = startRow, end_row=endRow, only_auto=onlyAuto , folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_autofit_workbook_columns(self):
        """
        Test case for cells_workbook_post_autofit_workbook_rows

        Autofit workbook rows.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        autoFitterOptions = None
        startcolumn = 1
        endcolumn = 100
        onlyAuto = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_autofit_workbook_columns(name, auto_fitter_options=autoFitterOptions, start_column = startcolumn, end_column=endcolumn, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_encrypt_document(self):
        """
        Test case for cells_workbook_post_encrypt_document

        Encript document.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        encryption = WorkbookEncryptionRequest(key_length = 128)
        encryption.password = "123456"
        encryption.encryption_type = "XOR"
        autoFitterOptions = None
        startRow = 1
        endRow = 100
        onlyAuto = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_encrypt_document(name, encryption=encryption,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_import_data(self):
        """
        Test case for cells_workbook_post_import_data

        
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        data = ImportIntArrayOption()
        data.destination_worksheet = 'Sheet1'
        data.first_column = 1
        data.first_row = 3
        data.import_data_type = 'IntArray'
        data.is_vertical = True
        data.data = [1, 2, 3, 4]
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_import_data(name, import_data=data,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_protect_document(self):
        """
        Test case for cells_workbook_post_protect_document

        Protect document.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        protection = WorkbookProtectionRequest()
        protection.password = "123"
        protection.protection_type = "All"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_protect_document(name, protection=protection,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_workbook_calculate_formula(self):
        """
        Test case for cells_workbook_post_workbook_calculate_formula

        Calculate all formulas in workbook.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        options = CalculationOptions()
        options.ignore_error = True
        ignore_error = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbook_calculate_formula(name, options=options, ignore_error=ignore_error, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_workbook_get_smart_marker_result(self):
        """
        Test case for cells_workbook_post_workbook_get_smart_marker_result

        Smart marker processing result.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        xmlFile = "ReportData.xml"
        result = AuthUtil.Ready(self.api, name, folder)
        result = AuthUtil.Ready(self.api, xmlFile, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbook_get_smart_marker_result(name, xml_file=(folder + '/' + xmlFile), folder= folder)
        # self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_workbook_get_smart_marker_result_to_other_storage(self):
        """
        Test case for cells_workbook_post_workbook_get_smart_marker_result

        Smart marker processing result.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        xmlFile = "ReportData.xml"
        result = AuthUtil.Ready(self.api, name, folder)
        result = AuthUtil.Ready(self.api, xmlFile, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbook_get_smart_marker_result(name, xml_file=(folder + '/' + xmlFile), folder= folder,out_storage_name="DropBox")
        # self.assertEqual(result.code,200)
        pass
    def test_cells_workbook_post_workbook_settings(self):
        """
        Test case for cells_workbook_post_workbook_settings

        Update Workbook setting 
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        settings = WorkbookSettings()
        settings.auto_compress_pictures = True
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbook_settings(name, settings=settings,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_workbook_split(self):
        """
        Test case for cells_workbook_post_workbook_split

        Split workbook.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        format = "png"
        _from = 1
        to = 3
        horizontalResolution = 100
        verticalResolution = 90
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbook_split(name, format=format, _from=_from, to=to, horizontal_resolution=horizontalResolution, vertical_resolution=verticalResolution,  folder=folder,out_folder=folder)
        self.assertEqual(result.code,200)
        pass


    def test_cells_workbook_post_workbook_split_to_other_storage(self):
        """
        Test case for cells_workbook_post_workbook_split

        Split workbook.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        format = "png"
        _from = 1
        to = 3
        horizontalResolution = 100
        verticalResolution = 90
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbook_split(name, format=format, _from=_from, to=to, horizontal_resolution=horizontalResolution, vertical_resolution=verticalResolution,  folder=folder,out_folder=folder,out_storage_name="DropBox")
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_workbooks_merge(self):
        """
        Test case for cells_workbook_post_workbooks_merge

        Merge workbooks.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        formatmergeWith = "myDocument.xlsx"      
        result = AuthUtil.Ready(self.api, name, folder)
        result = AuthUtil.Ready(self.api, formatmergeWith, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbooks_merge(name,folder +'/'+ formatmergeWith,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_workbooks_merge_with_other_storage(self):
        """
        Test case for cells_workbook_post_workbooks_merge

        Merge workbooks.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        formatmergeWith = "myDocument.xlsx"      
        result = AuthUtil.Ready(self.api, name, folder)
        result = AuthUtil.Ready(self.api, formatmergeWith, folder,storage="DropBox")
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbooks_merge(name,folder +'/'+ formatmergeWith,  folder=folder,merged_storage_name="DropBox")
        self.assertEqual(result.code,200)
        pass
    def test_cells_workbook_post_workbooks_text_replace(self):
        """
        Test case for cells_workbook_post_workbooks_text_replace

        Replace text.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        oldValue = "!22"
        newValue = "22"    
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbooks_text_replace(name, oldValue,newValue,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_post_workbooks_text_search(self):
        """
        Test case for cells_workbook_post_workbooks_text_search

        Search text.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        text = "!test"      
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_workbooks_text_search(name, text,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_put_convert_workbook(self):
        """
        Test case for cells_workbook_put_convert_workbook

        Convert workbook from request content to some format.
        """
        fullfilename = os.path.dirname(os.path.realpath(__file__)) + "/../TestData/" + "Book1.xlsx"
        f = open(fullfilename, 'rb')
        workbook = f.read()
        f.close()
        format ='pdf'       
        password = None
        outPath = None      
        result = self.api.cells_workbook_put_convert_workbook(fullfilename,format=format)
        # self.assertEqual(result.code,200)
        pass
    def test_cells_workbook_put_convert_workbook_extend(self):
        """
        Test case for cells_workbook_put_convert_workbook

        Convert workbook from request content to some format.
        """
        fullfilename = os.path.dirname(os.path.realpath(__file__)) + "/../TestData/" + "Book1.xlsx"
        f = open(fullfilename, 'rb')
        workbook = f.read()
        f.close()
        format ='pdf'       
        password = None
        outPath = None      
        result = self.api.cells_workbook_put_convert_workbook(fullfilename,format=format, extended_query_parameters ={"OnePagePerSheet":"false"})
        # self.assertEqual(result.code,200)
        pass
    def test_cells_workbook_put_convert_workbook_to_other_storage(self):
        """
        Test case for cells_workbook_put_convert_workbook

        Convert workbook from request content to some format.
        """
        fullfilename = os.path.dirname(os.path.realpath(__file__)) + "/../TestData/" + "Book1.xlsx"
        f = open(fullfilename, 'rb')
        workbook = f.read()
        f.close()
        format ='pdf'       
        password = None
        outPath = "Freeing/test_python_book1.pdf"
        result = self.api.cells_workbook_put_convert_workbook(fullfilename,format=format,out_path=outPath,storage_name="DropBox" )
        # self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_put_document_protect_from_changes(self):
        """
        Test case for cells_workbook_put_document_protect_from_changes

        Protect document from changes.
        """
        name ='Book1.xlsx'       
        folder = "PythonTest"
        password = PasswordRequest()
        password.password = "123456"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_put_document_protect_from_changes(name, password=password,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_put_workbook_create(self):
        """
        Test case for cells_workbook_put_workbook_create

        Create new workbook using deferent methods.
        """
        templateFile ='Book1.xlsx'       
        folder = "PythonTest"
        name = "NewBook" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xlsx"    
        dataFile = "ReportData.xml"  
        AuthUtil.Ready(self.api,templateFile, folder)
        AuthUtil.Ready(self.api,dataFile, folder)
        template_file = folder + "/" + templateFile
        data_file = folder + "/" + dataFile
        result = self.api.cells_workbook_put_workbook_create(name, template_file=template_file, data_file=data_file,  folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_put_workbook_background(self):
        """
        Test case for test_cells_workbook_put_workbook_background

        Set workbook background image.
        """
        name = "Book1.xlsx"
        sheet_name ='Sheet1' 
        isVisible = True
        sheettype = "VB" 
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        fullfilename = os.path.dirname(os.path.realpath(__file__)) + "/../TestData/" + "WaterMark.png"
        f = open(fullfilename, 'rb')
        png = f.read()
        f.close()
        result = self.api.cells_workbook_put_workbook_background(name,  png, folder=folder)
        self.assertEqual(result.code,200)
        pass

    def test_cells_workbook_delete_workbook_background(self):
        """
        Test case for test_cells_workbook_delete_workbook_background

        Set workbook background image.
        """
        name = "Book1.xlsx"
        sheet_name ='Sheet1' 
        isVisible = True
        sheettype = "VB" 
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_delete_workbook_background(name,   folder=folder)
        self.assertEqual(result.code,200)
        pass
    def test_cells_workbook_pagecount(self):
        """
        Test case for cells_worksheets_put_worksheet_freeze_panes

        Set freeze panes
        """
        name = "Book1.xlsx"
       
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_get_page_count(name,  folder=folder)
        self.assertGreater(result,0)
        pass
    def test_cells_workbook_post_digital_signature(self):
        """
        Test case for test_cells_workbook_post_digital_signature

        Set workbook background image.
        """
        name = "Book1.xlsx"
        pfx_name ='roywang.pfx' 
        password = '123456'
        folder = "PythonTest"
        result = AuthUtil.Ready(self.api, name, folder)
        result = AuthUtil.Ready(self.api, pfx_name, "")
        self.assertTrue(len(result.uploaded)>0) 
        result = self.api.cells_workbook_post_digital_signature(name,  pfx_name, password,folder=folder)
        self.assertEqual(result.code,200)
        pass    
if __name__ == '__main__':
    unittest.main()
