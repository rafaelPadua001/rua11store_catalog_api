<template>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8" xl="6">
        <v-card class="pa-4">
          <v-card-title class="d-flex justify-center">
            <h1 class="text-h4">Categories Management</h1>
          </v-card-title>
          
          <v-card-actions class="d-flex justify-end mb-4">
            <v-btn color="primary" @click="newItem">
              <v-icon left>mdi-plus</v-icon>
              Add Category
            </v-btn>
          </v-card-actions>
          
          <v-data-table
            :headers="headers"
            :items="allCategories"
            :items-per-page="10"
            class="elevation-1"
            item-key="id"
            fixed-header
            height="500"
            :loading="loading"
            loading-text="Loading categories..."
          >
            <!-- Category name with hierarchy indicator -->
            <template v-slot:item.name="{ item }">
              <div class="d-flex align-center" :style="{ 'padding-left': item.isSubcategory ? '32px' : '0' }">
                <v-icon
                  v-if="item.isSubcategory"
                  small
                  class="mr-2"
                >
                  mdi-subdirectory-arrow-right
                </v-icon>
                <span :class="{'font-weight-bold': !item.isSubcategory}">
                  {{ item.name }}
                </span>
              </div>
            </template>
            
            <!-- Category type chip -->
            <template v-slot:item.type="{ item }">
              <v-chip small :color="item.isSubcategory ? 'teal lighten-4' : 'blue lighten-4'">
                {{ item.isSubcategory ? 'Subcategory' : 'Category' }}
              </v-chip>
            </template>
            
            <!-- Actions column -->
            <template v-slot:item.actions="{ item }">
              <v-tooltip bottom>
                <template v-slot:activator="{ props: activatorProps }">
                  <v-icon 
                    small 
                    class="mr-2" 
                    v-bind="activatorProps" 
                    @click.stop="editItem(item)"
                  >
                    mdi-pencil
                  </v-icon>
                </template>
                <span>Edit</span>
              </v-tooltip>
              <v-tooltip bottom>
                <template v-slot:activator="{ props: activatorProps }">
                  <v-icon 
                    small 
                    v-bind="activatorProps" 
                    @click.stop="deleteItem(item)"
                  >
                    mdi-delete
                  </v-icon>
                </template>
                <span>Delete</span>
              </v-tooltip>
            </template>
          </v-data-table>
        </v-card>
        
        <!-- Edit/Create Dialog -->
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title class="headline">{{ formTitle }}</v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-select
                      v-model="editedItem.isSubcategory"
                      :items="categoryTypes"
                      label="Category Type"
                      item-text="text"
                      item-value="value"
                      outlined
                      dense
                    ></v-select>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      v-model="editedItem.name"
                      label="Category Name"
                      outlined
                      dense
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" v-if="editedItem.isSubcategory">
                    <v-select
                      v-model="editedItem.parentId"
                      :items="mainCategories"
                      label="Parent Category"
                      item-text="name"
                      item-value="id"
                      outlined
                      dense
                    ></v-select>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="grey darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="primary" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </template>
  
  <script>
  export default {
    data() {
      return {
        loading: false,
        dialog: false,
        editedIndex: -1,
        editedItem: {
          id: null,
          name: '',
          isSubcategory: false,
          parentId: null
        },
        defaultItem: {
          id: null,
          name: '',
          isSubcategory: false,
          parentId: null
        },
        headers: [
          { text: 'ID', value: 'id', width: '80px', align: 'center' },
          { text: 'Name', value: 'name', width: '250px' },
          { text: 'Type', value: 'type', width: '150px', align: 'center' },
          { text: 'Actions', value: 'actions', width: '120px', align: 'center', sortable: false }
        ],
        categoryTypes: [
          { text: 'Main Category', value: false },
          { text: 'Subcategory', value: true }
        ],
        categories: []
      }
    },
    computed: {
      allCategories() {
        // Ordena as categorias para agrupar subcategorias com suas pais
        const sorted = [];
        this.categories.forEach(category => {
          if (!category.isSubcategory) {
            sorted.push(category);
            // Adiciona subcategorias imediatamente após a categoria pai
            this.categories
              .filter(sub => sub.isSubcategory && sub.parentId === category.id)
              .forEach(sub => sorted.push(sub));
          }
        });
        return sorted;
      },
      mainCategories() {
        return this.categories.filter(c => !c.isSubcategory);
      },
      formTitle() {
        return this.editedIndex === -1 ? 'New Category' : 'Edit Category';
      }
    },
    created() {
      this.loadCategories();
    },
    methods: {
      async loadCategories() {
        this.loading = true;
        try {
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 500));
          
          // Mock data - replace with your API call
          this.categories = [
            { id: 1, name: 'Electronics', isSubcategory: false, parentId: null },
            { id: 2, name: 'Computers', isSubcategory: true, parentId: 1 },
            { id: 3, name: 'Smartphones', isSubcategory: true, parentId: 1 },
            { id: 4, name: 'Clothing', isSubcategory: false, parentId: null },
            { id: 5, name: 'Men', isSubcategory: true, parentId: 4 },
            { id: 6, name: 'Women', isSubcategory: true, parentId: 4 }
          ];
        } catch (error) {
          console.error("Error loading categories:", error);
        } finally {
          this.loading = false;
        }
      },
      
      newItem() {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.dialog = true;
      },
      
      editItem(item) {
        this.editedIndex = this.categories.indexOf(item);
        this.editedItem = Object.assign({}, item);
        this.dialog = true;
      },
      
      deleteItem(item) {
        const index = this.categories.indexOf(item);
        if (confirm('Are you sure you want to delete this item?')) {
          // Also delete any subcategories if this is a parent
          if (!item.isSubcategory) {
            this.categories = this.categories.filter(c => c.parentId !== item.id);
          }
          this.categories.splice(index, 1);
        }
      },
      
      close() {
        this.dialog = false;
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem);
          this.editedIndex = -1;
        });
      },
      
      save() {
        if (this.editedIndex > -1) {
          // Update existing item
          Object.assign(this.categories[this.editedIndex], this.editedItem);
        } else {
          // Add new item
          this.editedItem.id = Math.max(...this.categories.map(c => c.id), 0) + 1;
          this.categories.push(this.editedItem);
        }
        this.close();
      }
    }
  }
  </script>
  
  <style scoped>
  .v-data-table {
    width: 100%;
  }
  
  .v-data-table >>> .v-data-table-header {
    background-color: #f5f5f5;
  }
  
  .v-data-table >>> .v-data-table-header th {
    font-weight: 600;
  }
  </style>