<template>
  <v-container>
    <v-row justify="center" class="mt-4">
      <v-col cols="12" md="6">
        <v-defaults-provider :defaults="{ VBtn: { variant: 'outlined', color: '#eee' } }">
          <v-sheet class="mx-auto overflow-hidden" rounded="xl">
            <v-carousel v-model="currentIndex" class="mx-auto" progress="purple" show-arrows="hover" hide-delimiter
              height="auto">
              <!-- Primeira imagem: thumbnail -->
              <v-carousel-item class="carousel-img" v-if="product.thumbnail_path" :src="product.thumbnail_path"
                :alt="product?.seo?.slug">
                <v-chip class="ma-2" v-if="product.product_quantity == 0" color="error">Esgotado</v-chip>
              </v-carousel-item>

              <!-- Outras imagens -->
              <v-carousel-item class="carousel-img" v-for="(img, index) in product.images" :key="index" :src="img.url">

              </v-carousel-item>
            </v-carousel>

            <!-- Overlay com legenda -->
            <v-overlay :scrim="false"
              content-class="d-flex flex-column align-center justify-space-between pointer-pass-through py-3" contained
              model-value no-click-animation persistent>

            </v-overlay>
          </v-sheet>
          <div class="text-center">
            <v-chip :text="`${currentIndex + 1} / ${product.images.length + 1}`" color="deep-purple" size="small"
              variant="flat"></v-chip>
          </div>
        </v-defaults-provider>
      </v-col>
      <v-col cols="12" md="6" class="px-4">
        <div class="text-center text-md-start">
          <span class="text-h3 text-sm-h4 font-weight-bold">
            {{ product.name }}
          </span>
        </div>
        <div class="text-center text-md-start mt-2">
          <span class="text-h6 text-md-h5">
            R$ {{ product.price }}
          </span>
        </div>

        <div class="d-flex flex-column flex-sm-row align-center justify-center justify-md-start mt-4"
          style="gap: 10px;">
          <v-btn color="black" @click="addItemCart(product)">
            <v-icon size="x-large">mdi-cart-plus</v-icon>
            Adicionar ao carrinho
          </v-btn>
          <v-btn color="success" @click="goToWhatsApp">
            <v-icon size="x-large">mdi-whatsapp</v-icon>
            Pedir pelo Whatsapp
          </v-btn>
        </div>

        <div class="mt-4">
          <span class="text-subtitle"><strong>Variatons:</strong></span>
          <!-- Agrupamento: percorre cada tipo (ex: 'Color', 'Size') -->
          <template v-for="(items, type) in groupedVariations" :key="type">
            <!-- só mostra o grupo quando existir items -->
            <div v-if="items && items.length" class="mb-3">
              <strong class="mr-2">{{ type }}:</strong>

              <v-chip v-for="(variation, i) in items.filter(v => v && (v.quantity === undefined || v.quantity > 0))"
                :key="i" class="ma-1" :color="type === 'Color' ? variation.value : undefined"
                @click="selectVariation(variation)" clickable outlined small>
                <span v-if="type === 'Color'">
                  {{ colorNames[variation.value?.toUpperCase()] || variation.value }}
                </span>

                <span v-else>
                  {{ variation.value }}
                </span>
              </v-chip>

            </div>
          </template>
        </div>

        <!-- Mostrar apenas se houver pelo menos 1 variação selecionada -->
        <div class="d-flex flex-wrap align-center" v-if="selectedVariations && selectedVariations.length">
          <strong class="mr-3">Selected:</strong>

          <div class="d-flex flex-wrap align-center">
            <div v-for="(selectedVariation, index) in selectedVariations"
              :key="`selected-${index}-${selectedVariation.value}`" class="mr-2 d-flex align-center">
              <span v-if="selectedVariation.variation_type === 'Size'">
                <strong>{{ selectedVariation.value }}</strong>
              </span>

              <span v-else>
                <strong>
                  {{ colorNames[selectedVariation.value?.toUpperCase()] || selectedVariation.value }}
                </strong>

              </span>

              <!-- Quantity field-->
              <v-text-field v-model.number="selectedVariation.input_quantity" type="number" min="0"
                :max="selectedVariation.stock_quantity" density="compact" hide-details style="max-width: 90px;"
                label="Qtd:" />

            </div>
          </div>
        </div>

      </v-col>

    </v-row>


    <!-- Sugestoes de produtos -->
    <v-row>
      <v-col cols="12">
        <!--  <v-card>
          <v-toolbar color="transparent">
            <v-toolbar-title>
              <span class="text-h8">Combine com...</span>
            </v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-card>
              produtos
            </v-card>
            <v-card>
              produtos
            </v-card>
            <v-card>
              produtos
            </v-card>
            <v-card>
              produtos
            </v-card>
          </v-card-text>
        </v-card>-->
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <v-col cols="12">
        <v-card elevation="2" rounded="lg">
          <v-card-title>
            Descrição
          </v-card-title>
          <v-card-text>
            <v-card-text>
              <p class="text-body-2 text-md-body-1 text-justify">{{ product.description }}</p>
            </v-card-text>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <v-col cols="12">
        <v-card elevation="0">
          <v-card-title>
            Comments: ({{ this.product.comments?.length }})
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text>
            <v-row no-gutters justify="center">
              <v-col cols="3" md="1">
                <v-avatar color="grey" rounded="10" size="75">
                  <v-img height="100%" v-if="authUser?.[0]?.profile?.avatar_url" :src="authUser[0].profile.avatar_url"
                    :alt="authUser[0].profile.avatar_url" contain></v-img>
                  <v-img height="100%" v-else src="https://cdn.vuetifyjs.com/images/cards/server-room.jpg"
                    contain></v-img>
                </v-avatar>
              </v-col>
              <v-col cols="6" md="1">
                <v-list-item class=""
                  :subtitle="`${authUser?.[0]?.addresses?.[0]?.city}, ${authUser?.[0]?.addresses?.[0]?.state}`"
                  :title="authUser?.[0]?.profile?.username">

                </v-list-item>
              </v-col>

              <v-col cols="8" md="7">
                <div class="d-flex align-end">
                  <v-textarea v-model="message" placeholder="Write a comment..." auto-grow rows="3" max-rows="4"
                    hide-details variant="outlined" density="comfortable" class="flex-grow-1" />
                </div>
              </v-col>
              <v-col cols="8" md="9">
                <div class="d-flex justify-end">
                  <v-btn color="primary" @click="submitComment()">Comment</v-btn>
                </div>

              </v-col>
            </v-row>

          </v-card-text>
          <v-card-text v-if="product?.comments?.length">
            <v-list density="compact" lines="two">
              <v-list-item v-for="(comment, index) in product.comments" :key="index" class="border-b border-gray-200">
                <template #prepend>
                  <v-avatar size="50">
                    <v-img v-if="comment.avatar_url" :src="comment.avatar_url" :alt="comment.username"></v-img>
                    <v-img v-else src="https://cdn.vuetifyjs.com/images/profiles/marcus.jpg"></v-img>
                  </v-avatar>
                </template>

                <v-list-item-title class="font-semibold">
                  {{ comment.user_name }}
                </v-list-item-title>

                <v-list-item-subtitle>
                  {{ comment.comment }}
                </v-list-item-subtitle>


                <div justify="justify-end">
                  {{ comment.updated_at }}
                </div>


                <template #append v-if="authUser?.[0]?.id === (comment.userId || comment.user_id)">
                  <div class="d-flex align-center">
                    <v-btn size="x-small" variant="plain" color="primary" @click="editComment(comment)">
                      Edit
                    </v-btn>
                    <v-btn size="x-small" variant="plain" color="error" @click="removeComment(comment.id)">
                      Remove
                    </v-btn>
                  </div>
                </template>


              </v-list-item>
            </v-list>
          </v-card-text>

          <v-card-text v-else>


          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="editCommentDialog">
      <commentForm :authUser="authUser" :editedComment="editedComment" :comment="editedComment.comment"
        @save="submitComment" @close="editCommentDialog = false" />
    </v-dialog>

    <transition name="fade">
      <v-alert v-if="alert" class="notification" type="success" variant="elevated" elevation="8" border="start"
        :text="alertMessage" title="Produto adicionado ao carrinho" />
      <v-alert v-else-if="alertError" class="notification" type="error" elevation="8" border="start"
        :text="alertMessage" title="Erro ao adicionar o produto ao carrinho">
      </v-alert>
    </transition>
  </v-container>
</template>

<script>
import axios from "axios";
import { useSeo } from "@/useSeo";
import commentForm from "@/pages/comments/client/commentForm.vue";



const api = axios.create({
  baseURL:
    window.location.hostname === "localhost"
      ? "http://localhost:5000"
      : "https://rua11store-catalog-api-lbp7.onrender.com",
  headers: { "Content-Type": "application/json" },
});
const token = localStorage.getItem('access_token') || localStorage.getItem('token');
export default {
  components: {
    commentForm,
  },
  data() {
    return {
      product: { images: [], comments: [], variations: [] },
      currentIndex: 0,
      alert: null,
      alertError: null,
      alertMessage: '',
      authUser: [],
      message: '',
      editCommentDialog: false,
      editedIndex: -1,
      editedComment: {},
      comments: [],
      colorNames: {
        "#000000": "Preto",
        "#FFFFFF": "Branco",
        "#FF0000": "Vermelho",
        "#EB0909": "Vermelho",
        "#00FF00": "Verde",
        "#0000FF": "Azul",
        "#FFFF00": "Amarelo",
        "#FF00FF": "Rosa",
        "#730CF8": "Roxo",
        "#00FFFF": "Ciano",
        "#808080": "Cinza",
        // coloque aqui os HEX que seu catálogo usa
      },
      selectedVariations: [],

    };
  },
  async created() {
    await this.loadProduct();
    console.log(this.loadProduct());
    await this.loadAuthUser();
    this.comments = this.product.comments || [];

    if (window.fbq && this.product) {
      fbq('track', 'ViewContent', {
        content_ids: [this.product.id],
        content_type: 'product',
        content_name: this.product.name,
        valu: this.product.price,
        currentcy: 'BRL'
      });
    }
  },
  computed: {
    groupedVariations() {
      const variations = Array.isArray(this.product?.variations)
        ? this.product.variations
        : [];

      const groups = {};

      variations.forEach(v => {
        if (!v) return;

        const type = v.variation_type || "other";

        if (!groups[type]) groups[type] = [];

        groups[type].push(v);
      })
      return groups;
    },
    totalInputQuantity() {
      return this.selectedVariations.reduce(
        (sum, v) => sum + (v.input_quantity || 0),
        0
      )
    },
    totalStockQuantity() {
      return this.selectedVariations.reduce(
        (sum, v) => sum + (v.stock_quantity || 0),
        0
      )
    },
    currentImage() {
      // primeira é thumbnail, depois imagens
      if (this.currentIndex === 0) {
        return { url: this.product.thumbnail_path, label: this.product.name };
      }
      return this.product.images[this.currentIndex - 1] || null;
    },
  },
  watch: {
    "$route.params.slug": {
      immediate: false,
      handler: async function (newSlug, oldSlug) {
        if (newSlug !== oldSlug) {
          await this.loadProduct();
        }
      },
    },
  },
  methods: {
    async loadProduct() {
      const pageSlug = this.$route.params.slug;
      try {
        const response = await api.get(`/products/product/${pageSlug}`);
        this.product = response.data;

        if (this.product.seo) {
          const { setSeo } = useSeo();
          setSeo(this.product);
        }
      } catch (error) {
        console.error("Erro ao buscar produto:", error);
      }
    },
    async loadAuthUser() {
      try {
        const response = await api.get('/client/get-logged-client', {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        if (response.status === 200 || response.status === 201) {
          return this.authUser.push(response.data);

        }
        else {
          console.log('perfil de usuario não encontrado');
        }
      }
      catch (e) {
        console.log('Perfil de usuário não encontrado, tente novamente.', e);
      }
    },
    async selectVariation(variation) {
      const existingIndex = this.selectedVariations.findIndex(
        v => v.variation_type === variation.variation_type
      )

      const normalized = this.normalizeVariation(variation)

      if (existingIndex !== -1) {
        this.selectedVariations.splice(existingIndex, 1, normalized)
      } else {
        this.selectedVariations.push(normalized)
      }
    },
    normalizeVariation(variation) {
      return {
        ...variation,
        stock_quantity: variation.quantity,
        input_quantity: 0
      }
    },
    async addItemCart(product) {
      try {
        const token = localStorage.getItem('token') || localStorage.getItem('access_token');
        if (!token) {
          return alert('Você precisa estar logado...');
        }

        if (product.product_quantity == 0) {
          // console.log(this.alert);
          this.showNotification();
          return;
        }

        if (this.totalInputQuantity > this.totalStockQuantity) {
          alert('Não é permitido adicionar quantidade de variações maior que o estoque disponível');
          return;
        }

        const variationsPayload = this.selectedVariations
          .filter(v => v.input_quantity > 0)
          .map(v => ({
            variation_id: v.id,
            quantity: v.input_quantity,
            value: v.value
          }))

        if (variationsPayload.length === 0) {
          alert('Informe a quantidade de pelo menos uma variação');
        }


        const response = await api.post(`/cart/add-cart`, {
          product_id: product.id,
          selectedVariations: variationsPayload,
        },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });


        if (typeof window.fqb === 'function') {
          window.fbq("track", "AddToCart", {
            content_ids: [product.id],
            content_type: "product",
            content_name: product.name,
            value: product.price ?? 0,
            currency: "BRL"
          });

          this.showNotification();
        }
        console.log('Item adicionado');
      } catch (e) {
        console.log("erro ao inserir item no carrinho", e);
        //this.notification();
      }
    },
    showNotification() {
      if (this.product.product_quantity === 0) {
        this.alertMessage = "Produto sem estoque";
        this.alertError = true;
        setTimeout(() => {
          this.alertError = false
        }, 3000);
        return;
      }
      this.alertMessage = `Produto ${this.product.name} - R$ ${this.product.price} adicionado ao carrinho`;
      this.alert = true;
      setTimeout(() => {
        this.alert = false;
      }, 3000); //desaparece em 3 segundos;

    },
    goToWhatsApp() {
      const message = `Olá, tenho interesse no produto: ${this.product.name}`;
      const phone = "556191865680"; // seu número aqui
      window.open(
        `https://wa.me/${phone}?text=${encodeURIComponent(message)}`,
        "_blank"
      );
    },
    downloadApp() {
      window.open(
        "https://play.google.com/store/apps/details?id=sua.app",
        "_blank"
      );
    },
    async submitComment(updatedComment) {
      try {
        // Monta payload a partir do comentário atualizado
        const payload = {
          comment: this.message || updatedComment.comment,
          product_id: this.product.id,
          user_id: this.authUser?.[0]?.id,
          status: 'pending' || updatedComment.status,
          user_name: this.authUser?.[0]?.profile?.username || updatedComment.user_name,
          avatar_url: this.authUser?.[0]?.profile?.avatar_url || updatedComment.avatar_url,
        }

        let response;

        if (this.editedIndex !== -1) {
          // Atualiza comentário existente
          response = await api.put(`/comments/update/${updatedComment.id}`, payload, {
            headers: { 'Authorization': `Bearer ${token}` }
          });

          if (response.status === 200) {
            // Atualiza localmente
            const index = this.product.comments.findIndex(c => c.id === updatedComment.id);
            if (index !== -1) this.product.comments[index] = response.data;
            console.log('Comentário atualizado com sucesso:', response.data.comment);
            this.editedIndex = -1;
            this.message = '';
            this.editedComment = null;
          } else {
            console.log('Erro ao atualizar comentário:', response);
          }
        } else {
          // Cria novo comentário
          response = await api.post(`/comments/new`, payload, {
            headers: { 'Authorization': `Bearer ${token}` }
          });

          if (response.status === 200 || response.status === 201) {
            if (!this.product.comments) this.product.comments = [];
            this.product.comments.push(response.data.comment);
            console.log('Comentário adicionado com sucesso:', response.data.comment);
            this.editedIndex = -1;
            this.message = '';
            this.editedComment = null;
          } else {
            console.log('Erro ao registrar comentário:', response);
          }
        }

      } catch (e) {
        console.log('Erro ao registrar comentário', e);
      }
    },
    async editComment(comment) {
      // Usa o array correto
      const comments = comment || [];

      this.editedIndex = comment.id;

      if (this.editedIndex === -1) {
        console.warn('Comentário não encontrado:', comment);
        return;
      }

      this.editedComment = { ...comment };
      this.editCommentDialog = true;
    },
    async removeComment(id) {
      if (!confirm("Tem certeza que deseja remover este comentário permanentemente?")) return;

      try {
        const response = await api.delete(`/comments/delete/${id}`);

        if (Array.isArray(this.product.comments)) {
          // Encontrar o índice do comentário pelo id
          const index = this.product.comments.findIndex(c => c?.id === id);

          if (index > -1) {
            // Remove o comentário específico
            this.product.comments.splice(index, 1);
          } else {
            // Caso não encontre, faz uma filtragem completa
            this.product.comments = this.product.comments.filter(c => c?.id !== id);
            console.log('Comentário removido (via filtro).');
          }
        } else {
          console.warn('this.comments não é um array, não foi possível atualizar localmente.');
        }
      } catch (e) {
        console.error('Erro ao remover comentário, tente novamente.', e);
      }
    }

  },

};
</script>
<style scoped>
.carousel-img {
  object-fit: cover;
  width: 100%;
  height: auto;

}

@media (max-width: 650px) {
  .carousel-img {
    max-height: 500px;
  }
}

.v-btn {
  font-size: 0.9rem;
  padding: 8px 12px;
}

.notification {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 350px;
  z-index: 9999;
}

/*anima notificação */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s, transform 0.4s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20);
}
</style>