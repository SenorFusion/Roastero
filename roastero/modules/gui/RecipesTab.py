# PyQt imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Standard Library Imports
import os, json, time, webbrowser

# Local project imports
from ..gui.RecipeEditorWindow import RecipeEditor
from ..gui.CustomQtWidgets import RecipeModel

class RecipesTab(QWidget):
    def __init__(self, recipeObject, roastTabObject, MainWindowObject):
        super(RecipesTab, self).__init__()

        # Pass in recipe object
        self.recipe = recipeObject

        self.roastTab = roastTabObject

        self.MainWindow = MainWindowObject

        self.create_ui()

    def create_ui(self):
        """A method used to create the basic ui for the Recipe Tab."""
        self.layout = QGridLayout()

        # Create recipe browser.
        self.create_recipe_browser()
        self.layout.addWidget(self.recipeBrowser, 0, 0)
        self.layout.addWidget(self.createNewRecipeButton, 1, 0)

        # Create recipe window.
        self.create_recipe_window()
        self.create_recipe_buttons()
        self.layout.addLayout(self.recipeWindow, 0, 1)
        self.layout.addLayout(self.recipeButtonsLayout, 1, 1)

        # Set stretch so items align correctly.
        self.layout.setColumnStretch(1, 2)
        self.layout.setRowStretch(0, 3)

        # Create label to cover recipe info.
        self.recipeSelectionLabel = QLabel()
        self.recipeSelectionLabel.setObjectName("recipeSelectionLabel")
        self.recipeSelectionLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.recipeSelectionLabel, 0, 1)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def create_recipe_browser(self):
        """Creates the side panel to browse all the files in the recipe folder.
        This method also adds a button to create new recipes to the layout."""
        # Creates model with all information about the files in ./recipes
        self.model = RecipeModel()
        self.model.setRootPath('./recipes')

        # Create a TreeView to view the information from the model
        self.recipeBrowser = QTreeView()
        self.recipeBrowser.setModel(self.model)
        self.recipeBrowser.setRootIndex(self.model.index(os.path.expanduser('~/Documents/Roastero/recipes/')))
        self.recipeBrowser.setFocusPolicy(Qt.NoFocus)
        self.recipeBrowser.header().close()

        self.recipeBrowser.setAnimated(True)
        self.recipeBrowser.setIndentation(0)

        # Hides all the unecessary columns created by the model
        self.recipeBrowser.setColumnHidden(0, True)
        self.recipeBrowser.setColumnHidden(1, True)
        self.recipeBrowser.setColumnHidden(2, True)
        self.recipeBrowser.setColumnHidden(3, True)

        self.recipeBrowser.clicked.connect(self.on_recipeBrowser_clicked)

        # Add create new recipe button.
        self.createNewRecipeButton = QPushButton("NEW RECIPE")
        self.createNewRecipeButton.clicked.connect(self.create_new_recipe)

    def create_recipe_window(self):
        """Creates the whole right-hand side of the recipe tab. These fields are
        populated when a recipe is chosen from the left column."""
        # Create all of the gui Objects
        self.recipeWindow = QGridLayout()
        self.recipeNameLabel = QLabel("Recipe Name")
        self.recipeCreatorLabel = QLabel("Created by ")
        self.recipeTotalTimeLabel = QLabel("Total Time: ")
        self.recipeRoastTypeLabel = QLabel("Roast Type: ")
        self.beanRegionLabel = QLabel("Bean Region: ")
        self.beanCountryLabel = QLabel("Bean Country: ")
        self.recipeDescriptionBox = QTextEdit()
        self.recipeDescriptionBox.setReadOnly(True)
        self.recipeStepsTable = QTableWidget()

        # Set options for recipe table.
        self.recipeStepsTable.setShowGrid(False)
        self.recipeStepsTable.setAlternatingRowColors(True)
        self.recipeStepsTable.setCornerButtonEnabled(False)
        self.recipeStepsTable.horizontalHeader().setSectionResizeMode(1)
        self.recipeStepsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.recipeStepsTable.setSelectionMode(QAbstractItemView.NoSelection)

        # Assign Object Names for qss
        self.recipeNameLabel.setObjectName("RecipeName")
        self.recipeCreatorLabel.setObjectName("RecipeCreator")
        self.recipeTotalTimeLabel.setObjectName("RecipeTotalTime")
        self.recipeRoastTypeLabel.setObjectName("RecipeRoastType")
        self.beanRegionLabel.setObjectName("RecipeBeanRegion")
        self.beanCountryLabel.setObjectName("RecipeBeanCountry")
        self.recipeStepsTable.setObjectName("RecipeSteps")

        # Add objects to the layout
        self.recipeWindow.addWidget(self.recipeNameLabel, 0, 0, 1, 2)
        self.recipeWindow.addWidget(self.recipeCreatorLabel, 1, 0)
        self.recipeWindow.addWidget(self.recipeRoastTypeLabel, 2, 0)
        self.recipeWindow.addWidget(self.recipeTotalTimeLabel, 3, 0)
        self.recipeWindow.addWidget(self.beanRegionLabel, 4, 0)
        self.recipeWindow.addWidget(self.beanCountryLabel, 5, 0)
        self.recipeWindow.addWidget(self.recipeDescriptionBox, 7, 0)
        self.recipeWindow.addWidget(self.recipeStepsTable, 7, 1)

    def create_recipe_buttons(self):
        """Creates the button panel on the bottom to allow for the user to
        interact with the currently selected/viewed recipe."""
        self.recipeButtonsLayout = QGridLayout()
        self.recipeButtonsLayout.setSpacing(0)
        self.recipeRoastButton = QPushButton("ROAST NOW")
        self.editRecipeButton = QPushButton("EDIT")
        self.beanLinkButton = QPushButton("PURCHASE BEANS")

        # Assign object names for qss styling.
        self.recipeRoastButton.setObjectName("smallButton")
        self.beanLinkButton.setObjectName("smallButton")
        self.editRecipeButton.setObjectName("smallButton")
        self.createNewRecipeButton.setObjectName("smallButtonAlt")

        # Add spacer.
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.recipeButtonsLayout.addWidget(self.spacer)

        self.recipeRoastButton.clicked.connect(self.load_recipe)
        self.editRecipeButton.clicked.connect(self.open_recipe_editor)
        self.beanLinkButton.clicked.connect(self.open_link_in_browser)

        self.recipeButtonsLayout.addWidget(self.beanLinkButton, 0, 1)
        self.recipeButtonsLayout.addWidget(self.editRecipeButton, 0, 2)
        self.recipeButtonsLayout.addWidget(self.recipeRoastButton, 0, 3)

        # Disable buttons until recipe is selected.
        self.beanLinkButton.setEnabled(False)
        self.editRecipeButton.setEnabled(False)
        self.recipeRoastButton.setEnabled(False)

    def on_recipeBrowser_clicked(self, index):
        """This method is used when a recipe is selected in the left column.
        This method also enables the bottom button panel after a recipe has
        been selected."""
        indexItem = self.model.index(index.row(), 0, index.parent())

        self.selectedFilePath = self.model.filePath(indexItem)

        # Allow single click expanding of folders
        if os.path.isdir(self.selectedFilePath):
            if self.recipeBrowser.isExpanded(indexItem):
                self.recipeBrowser.collapse(indexItem)
            else:
                self.recipeBrowser.expand(indexItem)
        # Handles when a file is clicked
        else:
            # Load recipe information from file
            self.load_recipe_file(self.selectedFilePath)

            # Set lower buttons enabled once recipe is selected.
            self.beanLinkButton.setEnabled(True)
            self.editRecipeButton.setEnabled(True)
            self.recipeRoastButton.setEnabled(True)

            # Hide recipe selection label once a recipe is selected.
            self.recipeSelectionLabel.setHidden(True)

    def load_recipe_file(self, filePath):
        """Used to load file from a path into selected recipe object."""
        with open(filePath) as json_data:
            recipeObject = json.load(json_data)
        self.currentlySelectedRecipe = recipeObject
        self.currentlySelectedRecipePath = filePath
        self.load_recipe_information(self.currentlySelectedRecipe)

    def load_recipe_information(self, recipeObject):
        """Loads recipe information the into the right hand column fields.
        This method also populates the recipe steps table."""
        self.recipeNameLabel.setText(recipeObject["roastName"])
        self.recipeCreatorLabel.setText("Created by " +
            recipeObject["creator"])
        self.recipeRoastTypeLabel.setText("Roast Type: " +
            recipeObject["roastDescription"]["roastType"])
        self.beanRegionLabel.setText("Bean Region: " +
            recipeObject["bean"]["region"])
        self.beanCountryLabel.setText("Bean Country: " +
            recipeObject["bean"]["country"])
        self.recipeDescriptionBox.setText(recipeObject["roastDescription"]
            ["description"])
        self.currentBeanUrl = recipeObject["bean"]["source"]["link"]

        # Total Time
        t = time.strftime("%M:%S", time.gmtime(recipeObject["totalTime"]))
        self.recipeTotalTimeLabel.setText("Total Time: " + t + " minutes")

        # Steps spreadsheet
        self.recipeStepsTable.setRowCount(len(recipeObject["steps"]))
        self.recipeStepsTable.setColumnCount(3)
        self.recipeStepsTable.setHorizontalHeaderLabels(["Temperature",
            "Fan Speed", "Section Time"])

        for row in range(len(recipeObject["steps"])):

            sectionTimeWidget = QTableWidgetItem()
            sectionTempWidget = QTableWidgetItem()
            sectionFanSpeedWidget = QTableWidgetItem()

            sectionTimeWidget.setText(time.strftime("%M:%S",
                time.gmtime(recipeObject["steps"][row]["sectionTime"])))
            sectionFanSpeedWidget.setText(str(recipeObject["steps"][row]["fanSpeed"]))

            if 'targetTemp' in recipeObject["steps"][row]:
                sectionTempWidget.setText(str(recipeObject["steps"][row]["targetTemp"]))
            else:
                sectionTempWidget.setText("Cooling")

            # Set widget cell alignment.
            sectionTempWidget.setTextAlignment(Qt.AlignCenter)
            sectionFanSpeedWidget.setTextAlignment(Qt.AlignCenter)
            sectionTimeWidget.setTextAlignment(Qt.AlignCenter)

            # Add widgets
            self.recipeStepsTable.setItem(row, 0, sectionTempWidget)
            self.recipeStepsTable.setItem(row, 1, sectionFanSpeedWidget)
            self.recipeStepsTable.setItem(row, 2, sectionTimeWidget)

    def load_recipe(self):
        """Loads a JSON recipe file. This information is later used to populate
        the right-hand column."""
        if (self.recipe.check_recipe_loaded()):
            self.roastTab.clear_roast()

        self.recipe.load_recipe_json(self.currentlySelectedRecipe)
        self.roastTab.load_recipe_into_roast_tab()
        self.MainWindow.select_roast_tab()

    def open_link_in_browser(self):
        """Opens link to purchase the beans."""
        webbrowser.open(self.currentBeanUrl)

    def open_recipe_editor(self):
        """Method used to open Recipe Editor Window with an existing recipe."""
        self.editorWindow = RecipeEditor(recipeLocation = self.currentlySelectedRecipePath)
        self.editorWindow.exec_()
        self.load_recipe_file(self.selectedFilePath)


    def create_new_recipe(self):
        """Method used to open Recipe Editor Window for a new recipe."""
        self.editorWindow = RecipeEditor()
        self.editorWindow.exec_()
        self.load_recipe_file(self.selectedFilePath)

    def get_currently_selected_recipe(self):
        """returns currently selected recipe for use in Recipe Editor Window."""
        return self.currentlySelectedRecipe
