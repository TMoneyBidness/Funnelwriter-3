from ._anvil_designer import Home_newTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#############################################

from ..Company import Company
from ..Product import Product
from ..BrandTone import BrandTone
from ..Avatars import Avatars
from ..VSL_Elements import VSL_Elements
from ..VideoSalesLetter import VideoSalesLetter
from ..FinalProduct import FinalProduct
####################


class Home_new(Home_newTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.users.login_with_form()
    self.indeterminate_1.visible = False
    self.free_navigate_label.visible = False
    self.status.text = 'Idle'
    self.youtube_intro_video.visible = False
    self.nav_button_company_to_products.visible = False
    self.add_another_product_panel_1.visible = False
    self.add_another_product_panel_2.visible = False
    self.add_another_product_panel_3.visible = False
    self.add_another_product_panel_4.visible = False
    
    # Get the current user
    current_user = anvil.users.get_user()
    user_table_name = current_user['user_id']
    
    # Get the table for the current user
    user_table = getattr(app_tables, user_table_name)

  def go_get_all_assets_click(self, **event_args):
    with anvil.server.no_loading_indicator:
      # This method should handle the UI logic
      print("Go Get All 1st Draft Assets")
    
      # Stop the function if any of the fields are empty
      if not self.company_name_input.text or not self.company_url_input.text or not self.product_1_name_input.text:
          anvil.js.window.alert("Please fill in all the required fields before generating the full description.")
          return

      else:
        self.indeterminate_1.visible = True
        self.free_navigate_label.visible = True
        self.status.text = 'Researching'

        # Load stuff        
        current_user = anvil.users.get_user()
        user_table_name = current_user['user_id']
        # Get the table for the current user
        user_table = getattr(app_tables, user_table_name)
    
        # COMPANY NAME
        company_name = self.company_name_input.text
        # Save company name
        company_name_row = user_table.get(variable='company_name')
        company_name_row['variable_value'] = company_name
        company_name_row.update()
        
        # COMPANY URL
        company_url = self.company_url_input.text
        # Save company url
        company_url_row = user_table.get(variable='company_url')
        company_url_row['variable_value'] = company_url
        company_url_row.update()

        # PRODUCT 1 NAME
        product_1_name = self.product_1_name_input.text
        # Save product 1 name
        product_1_row = user_table.get(variable='product_1')
        product_1_row['variable_title'] = product_1_name
        product_1_row.update()

        # PRODUCT 1 URL
        product_1_url = self.product_1_url_input.text
        # Save product 1 url
        product_1_url_row = user_table.get(variable='product_1_url')
        product_1_url_row['variable_value'] = product_1_url
        product_1_url_row.update()

      # LAUNCH THE BACKGROUND TASKS
       # Launch the background task for company summary
        anvil.server.call('launch_draft_company_summary',user_table, company_name, company_url)
        print("Company Research Started")

        # Launch the background task for brand tone
        anvil.server.call('launch_draft_brand_tone_research', user_table,company_url)
        print("Brand Tone Research Started")
       
        # Launch the background task for product research
        anvil.server.call('launch_draft_deepdive_product_1_generator',user_table,company_name,product_1_name,product_1_url)
        print("Deep Dive Product Research Started") 
      
     

  # NAVIGATION
  
 ### Show Other Panels
  def add_another_product_panel_1_click(self, **event_args):
    self.add_another_product_panel_1.visible = True

  def add_another_product_panel_2_click(self, **event_args):
    self.add_another_product_panel_2.visible = True

  def add_another_product_panel_3_click(self, **event_args):
    self.add_another_product_panel_3.visible = True

  def add_another_product_panel_4_click(self, **event_args):
    self.add_another_product_panel_4.visible = True

  # NAVIGATION
  
  def home_asset_link_copy_click(self, **event_args):
    open_form("Home")

  def product_asset_link_click(self, **event_args):
    product=Product()
    self.content_panel.clear()
    self.content_panel.add_component(product)

  def company_asset_link_click(self, **event_args):
    company=Company()
    self.content_panel.clear()
    self.content_panel.add_component(company)

  def brand_tone_asset_link_click(self, **event_args):
    brandtone=BrandTone()
    self.content_panel.clear()
    self.content_panel.add_component(brandtone)

  def avatars_asset_link_click(self, **event_args):
    avatars=Avatars()
    self.content_panel.clear()
    self.content_panel.add_component(avatars)

  def finalproduct_page_link_click(self, **event_args):
    finalproduct=FinalProduct()
    self.content_panel.clear()
    self.content_panel.add_component(finalproduct)

  def nav_button_to_company_click(self, **event_args):
    company = Company()
    self.content_panel.clear()
    self.content_panel.add_component(company)


## FUNNELS
  def VSL_page_link_click(self, **event_args):
    vsl_elements = VSL_Elements()
    self.content_panel.clear()
    self.content_panel.add_component(vsl_elements)

 