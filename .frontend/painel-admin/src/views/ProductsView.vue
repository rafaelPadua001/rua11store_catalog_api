<template>
    <div>
      <h2>Lista de Produtos</h2>
      <p>Aqui você pode gerenciar os produtos.</p>
      
      <div v-if="loading">Carregando...</div> <!-- Spinner ou mensagem -->
      
      <ul v-if="!loading">
        <li v-for="produto in produtos" :key="produto.id">
          {{ produto.nome }} - {{ produto.preco }}
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const produtos = ref([]);
  const loading = ref(true);
  
  onMounted(async () => {
    try {
      const response = await axios.get('http://localhost:5000/produtos');  // URL da sua API
      produtos.value = response.data;
    } catch (error) {
      console.error("Erro ao carregar os produtos", error);
    } finally {
      loading.value = false;
    }
  });
  </script>
  