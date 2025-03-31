import { createRouter, createWebHistory } from 'vue-router';
import ProductsView from '../views/ProductsView.vue'; // Ajuste conforme sua estrutura de diretórios

const routes = [
  {
    path: '/',
    name: 'home',
    component: ProductsView, // O componente será exibido para a rota raiz
  },
  //Adicione outras rotas conforme necessário, por exemplo:
  {
    path: '/produtos',
    name: 'produtos',
    component: ProductsView,
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Usando BASE_URL do Vite
  routes,
});

export default router;
