<template>
    <v-app-bar app color="indigo" dark>
      <v-toolbar-title>
        <router-link to="/" class="white--text">Logo</router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text>
        <router-link to="/" class="white--text">Home</router-link>
      </v-btn>
      <v-btn text>
        <router-link to="/produtos" class="white--text">Produtos</router-link>
      </v-btn>
    </v-app-bar>
  </template>
  
  <script setup>
  // Aqui você pode adicionar lógica ou props se necessário
  </script>
  
  <style scoped>
  /* Estilos adicionais, se necessário */
  </style>
  