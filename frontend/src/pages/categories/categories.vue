<template>
  <v-row justify="center" no-gutters>
    <v-col cols="12" md="12" lg="10" xl="6">
      <v-card class="pa-4" elevation="0">
        <v-card-title class="d-flex justify-center">
          <h5>Categories Management</h5>
        </v-card-title>
        <v-divider></v-divider>

        <v-card-actions class="d-flex justify-end mb-4">
          <v-btn color="primary" @click="newItem">
            <v-icon left>mdi-plus</v-icon>
            Add Category
          </v-btn>
        </v-card-actions>

        <v-data-table :headers="headers" :items="visibleCategories" :items-per-page="10" class="elevation-1"
          item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading categories...">
          <template v-slot:item.name="{ item }">
            <div class="d-flex align-center" :style="{ 'padding-left': item.is_subcategory ? '32px' : '0' }">

              <v-icon v-if="!item.is_subcategory" @click="toggleCategory(item.id)" class="mr-2">
                {{ expandedCategories.includes(item.id) ? 'mdi-chevron-down' : 'mdi-chevron-right' }}
              </v-icon>

              <v-icon v-if="item.is_subcategory" small class="mr-2">
                mdi-subdirectory-arrow-right
              </v-icon>
              <span :class="{ 'font-weight-bold': !item.is_subcategory }">
                {{ item.name }}
              </span>
            </div>
          </template>

          <template v-slot:item.type="{ item }">
            <v-chip small :color="item.is_subcategory ? 'teal lighten-4' : 'blue lighten-4'">
              {{ item.is_subcategory ? 'Subcategory' : 'Category' }}
            </v-chip>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-icon small color="primary" @click.stop="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon small color="error" @click.stop="deleteItem(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card>

      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">{{ formTitle }}</v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <label>Select Category Type:</label>
                  <v-select v-model="editedItem.is_subcategory" :items="categoryTypes" item-text="title"
                    item-title="title" item-value="key" label="Category Type" outlined dense></v-select>

                </v-col>
                
                <v-col cols="12" v-if="editedItem.is_subcategory">
                  <label>Select Subcategory:</label>
                  <v-select v-model="editedItem.parent_id" :items="mainCategories" label="Parent Category"
                    item-title="name" item-text="name" item-value="id" outlined dense></v-select>
                </v-col>
                <label>Category Name:</label>
                <v-col cols="12">
                  <v-text-field v-model="editedItem.name" label="Category Name" outlined dense></v-text-field>
                </v-col>

              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-btn color="grey darken-1" text @click="close">Cancel</v-btn>
            <v-btn color="primary" text @click="save">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-col>
  </v-row>
</template>

<script>
import axios from 'axios';

const api = axios.create({
  baseURL: window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : 'https://rua11store-catalog-api-lbp7.onrender.com',
  headers: { 'Content-Type': 'application/json' }
});

export default {
  data() {
    return {
      loading: false,
      expandedCategories: [],
      dialog: false,
      editedIndex: -1,
      editedItem: { id: null, name: '', is_subcategory: null, parent_id: null },
      defaultItem: { id: null, name: '', is_subcategory: null, parent_id: null },
      headers: [
        // { text: 'ID', value: 'id', width: '80px', align: 'center' },
        { title: 'Name', key: 'name', width: '250px' },
        { title: 'Type', key: 'type', width: '150px', align: 'center' },
        { title: 'Actions', key: 'actions', width: '120px', align: 'center', sortable: false }
      ],
      categoryTypes: [
        { title: 'Main Category', key: false },
        { title: 'Subcategory', key: true }
      ],
      categories: []
    };
  },
  watch: {
    'editedItem.is_subcategory'(newVal) {
      if (!newVal) {
        this.editedItem.parent_id = null;
      }
    }
  },
  computed: {
    allCategories() {
      return this.categories.reduce((sorted, category) => {
        if (!category.is_subcategory) {
          sorted.push(category);
          sorted.push(...this.categories.filter(sub => sub.is_subcategory && sub.parent_id === category.id));
        }
        return sorted;
      }, []);
    },
    mainCategories() {
      return this.categories.filter(c => !c.is_subcategory);
    },
    visibleCategories() {
      return this.allCategories.filter(c =>
        !c.is_subcategory || this.expandedCategories.includes(c.parent_id)
      );
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
        const response = await api.get('/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error("Error loading categories:", error);
      } finally {
        this.loading = false;
      }
    },
    toggleCategory(categoryId) {
      const index = this.expandedCategories.indexOf(categoryId);

      if (index === -1) {
        this.expandedCategories.push(categoryId);
      }
      else {
        this.expandedCategories.splice(index, 1);
      }
    },
    newItem() {
      this.editedItem = { ...this.defaultItem };
      this.dialog = true;
    },
    editItem(item) {
      this.editedIndex = this.categories.findIndex(c => c.id === item.id);
      this.editedItem = { ...item };
      this.dialog = true;
    },
    async save() {
      try {
        const token = localStorage.getItem('access_token');

        if (!token) return this.$router.push('/login');

        const config = { headers: { 'Authorization': `Bearer ${token}` } };


        let payload = { ...this.editedItem };
        if (typeof payload.is_subcategory === 'object' && payload.is_subcategory !== null) {
          payload.is_subcategory = payload.is_subcategory.key;
        }

        let response;
        if (this.editedIndex === -1) {
          response = await api.post('/categories/', payload, config);
          this.categories.push(response.data.category);
        } else {
          response = await api.put(`/categories/${this.editedItem.id}`, payload, config);
          Object.assign(this.categories[this.editedIndex], response.data.category);
        }
        this.close();
      } catch (error) {
        console.error("Error saving category:", error.response?.data || error.message);
      }
    },
    async deleteItem(item) {
      if (!confirm('Are you sure you want to delete this item?')) return;
      try {
        await api.delete(`/categories/${item.id}`);
        this.categories = this.categories.filter(c => c.id !== item.id);
      } catch (error) {
        console.error("Error deleting category:", error);
      }
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = { ...this.defaultItem };
        this.editedIndex = -1;
      });
    }
  }
};
</script>
