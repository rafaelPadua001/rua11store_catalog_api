<template>
    <v-row justify="center">
        <v-col cols="12" md="12" lg="10" xl="10" sm="12">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">Orders Management</h1>
                </v-card-title>

                <!-- <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newProduct" disabled>
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions> -->

                <v-data-table :headers="headers" :items="orders" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading deliveries...">
                    <!-- Exibe imagens de produtos -->
                    <!-- <template v-slot:item.image="{ item }">
                        <v-img v-if="item.image_path" :src="getProductImage(item.image_path, item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template> -->

                    <!-- Exibe a descrição do produto -->
                    <template v-slot:item.description="{ item }">
                        <span v-if="item.description && item.description.length > 100">
                            {{ item.description.substring(0, 38) }}...
                        </span>
                        <span v-else>
                            {{ item.description }}
                        </span>
                    </template>

                    <!-- Exibe a categoria -->
                    <!-- <template v-slot:item.category="{ item }">
                        <span v-if="item && item.category_id">{{ getCategoryName(item.category_id) }}</span>
                        <span v-else>Sem Categoria</span>
                    </template> -->

                    <!-- Exibe os ícones de ações -->
                    <template v-slot:item.actions="{ item }">
                        <!-- Ícone de criar etiqueta  -->
                        <!-- <v-icon small @click.stop="createTag(item)">
                            mdi-
                        </v-icon> -->

                         <!-- Botão de buscar item no carrinho  -->
                        <v-icon small @click.stop="checkItemInCart(item)">
                            mdi-file-search
                        </v-icon>

                        <!-- <v-icon small @click.stop="shipmentGenerate(item)">
                            mdi-bookmark
                        </v-icon> -->

                         <!-- Ícone de criar etiqueta  -->
                        <!-- <v-icon small @click.stop="pdfTag(item)">
                            mdi-file-pdf-box
                        </v-icon> -->
                         <!-- Ícone de deletar produto  -->
                        <v-icon small @click.stop="deleteItemCart(item)">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>

                <v-dialog v-model="dialogCheckItems" max-width="600px">
                    <v-card>
                        <v-card-title>
                            <span class="headline">Detalhes do Produto</span>
                        </v-card-title>
                        

                        <v-card-subtitle>
                            <!-- {{ selectedOrderItems }} -->
                            <v-row v-for="(item, index) in selectedOrderItems" :key="index" class="mb-4">
                                <v-col cols="12" sm="6">
                                    <strong>Nome do Produto:</strong> {{ item.product_name }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Descrição:</strong> {{ item.product_description }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Quantidade:</strong> {{ item.quantity }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Preço Unitário:</strong> R$ {{ item.unit_price.toFixed(2) }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Preço Total:</strong> R$ {{ item.total_price.toFixed(2) }}
                                </v-col>
                            </v-row>

                        </v-card-subtitle>
<!-- 
                        <v-card-subtitle>
                            <v-row>
                                <v-col cols="12" sm="6">
                                    <strong>Nome do Destinatário:</strong> {{ cartItems.data.to.name }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Endereço:</strong> {{ cartItems.data.to.address }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Cidade:</strong> {{ cartItems.data.to.city }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Estado:</strong> {{ cartItems.data.to.state }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Telefone:</strong> {{ cartItems.data.to.phone }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Email:</strong> {{ cartItems.data.to.email }}
                                </v-col>
                            </v-row>
                        </v-card-subtitle> -->

                        <v-card-actions>
                             <!-- Botão de compra de etiqueta no carrinho  -->
                              <!-- <v-btn small @click.stop="shipmentCheckout(cartItems.data)">
                                checkout
                              </v-btn> -->
                            
                            <v-btn color="green" text @click="dialogCheckItems = false">Close</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-card>


        </v-col>
    </v-row>
</template>


<script>
import axios from "axios";

const api = axios.create({
    baseURL: window.location.hostname === "localhost"
        ? "http://localhost:5000"
        : "https://rua11storecatalogapi-production.up.railway.app",
    headers: { "Content-Type": "application/json" },
});

export default {
    data() {
        return {
            loading: false,
            orders: [],
            selectedOrderItems: [],
            headers: [
                { text: "ID", value: "id" },
                { text: "User ID", value: "user_id" },
                { text: "Payment ID", value: "payment_id" },
                { text: "shipment info", value: "shipment_info" },
                { text: "Order date", value: "order_date" },
                { text: "status", value: "status" },
                { text: "Total amount", value: "total_amount" },
               
                //  { text: "Recipient Name", value: "recipient_name" },
                // { text: "Street", value: "street", align: "right" },
                // { text: "number", value: "number" },
                // { text: "complement", value: "complement" },
                // { text: "city", value: "city" },
                // { text: "state", value: "state" },
                // { text: "zipcode", value: "zip_code" },
                // { text: "bairro", value: "bairro" },
                // { text: "country", value: "country" },
                // { text: "phone", value: "phone" },
                // { text: "Email", value: "userEmail" },
                // { text: "Price", value: "price" },
                // { text: "Delivery", value: "delivery_id" },
                { text: "Actions", value: "actions", width: "120px", align: "center", sortable: false },
            ],
            isPaymentButtonPayTagDisabled: true,
            dialogCheckItems: false,
        };
    },
    // computed: {
    //     formattedPrice: {
    //         get() {
    //             return this.editedDeliveries && this.editedDeliveries.price !== undefined
    //                 ? Number(this.editedDeliveries.price).toFixed(2).replace(".", ",")
    //                 : "";
    //         },
    //         set(value) {
    //             let numericValue = parseFloat(value.replace(/[^0-9,]/g, "").replace(",", "."));
    //             this.editedDeliveries.price = isNaN(numericValue) ? 0.00 : numericValue;
    //         }
    //     }
    // },
    created() {
        this.loadOrders();
    },
    methods: {
        async loadOrders() {
            this.loading = true;
            try {
                const response = await api.get("order/get-orders");
                if (response.data && Array.isArray(response.data)) {
                    this.orders = response.data.flat().map(order => ({
                        id: order.id,
                        user_id: order.user_id,
                        payment_id: order.payment_id,
                        shipment_info: order.shipment_info,
                        order_date: order.order_date,
                        status: order.status,
                        total_amount: order.total_amount,
                        items: order.items

                    }));

                    console.log(response.data);
                } else {
                    console.error("Resposta não contém um array de entregas:", response.data);
                }
            } catch (error) {
                console.error("Erro ao carregar entregas:", error);
            } finally {
                this.loading = false;
            }
        },
        // getCategoryName(categoryId) {
        //     // Implemente aqui a lógica para buscar o nome da categoria baseado no categoryId
        //     return "Categoria Exemplo"; // Exemplo de retorno
        // },
        // async createTag(item) {
        //     try {
        //         const response = await api.post('/melhorEnvio/createTag', item);

        //         // Exibindo a resposta no console. Normalmente, a resposta está em response.data
        //         console.log('Resposta da API:', response.data); // Isso é geralmente a parte importante

        //         if (response.data.message == 'Envio criado com sucesso. Aguarde pagamento.') {
        //             this.isPaymentButtonPayTagDisabled = false;
        //             this.$toast.success('Etiqueta enviada com sucesso');
        //         }
        //         else {
        //             this.$toast.error('Algo deu errado. Por favor, tente novamente.');
        //         }
        //         // Exibe uma mensagem de sucesso

        //     } catch (error) {
        //         console.log('Erro ao enviar os dados da etiqueta:', error);
        //         this.$toast.error('Erro ao enviar os dados para o backend');
        //     }
        // },
        async checkItemInCart(item) {
          this.selectedOrderItems = item.items;
          console.log(this.selectedOrderItems);
          this.dialogCheckItems = true
        },
        // async shipmentCheckout(item) {
        //     console.log(item.id);
        //     try {
        //         const response = await api.post(`/melhorEnvio/shipmentCheckout`, {
        //             melhorenvio_id: item.id
        //         }, {
        //             headers: {
        //                 'Content-Type': 'application/json'
        //             }
        //         });



        //         if (response.status === 200 && response.data && response.data.status === 'success') {
        //             // this.$toast.success('O item está no carrinho');
        //             //window.alert('O item está no carrinho');
        //             this.cartItems = response.data;

        //             this.dialogCheckItemCart = true;
        //         } else {
        //             this.$toast.info('O item não está no carrinho');
        //         }

        //     } catch (error) {
        //         // Verifique se o erro contém a propriedade response
        //         if (error.response) {
        //             window.alert('item não encontrado no carrinho:', error.response.data);
        //             this.$toast.error('Erro ao verificar item no carrinho');
        //         } else {
        //             // Se não houver response, logue o erro simples
        //             console.log('Erro desconhecido:', error);
        //            // this.$toast.error('Erro desconhecido');
        //         }
        //     }
        // },
        // async shipmentGenerate(item){
        //     console.log(item);
        //     try{
        //         const response = await api.post(`/melhorEnvio/shipmentGenerate`, {
        //             melhorenvio_id: item.melhorenvio_id
        //         }, {
        //             headers: {
        //                 'Content-Type': 'application/json'
        //             }
        //         });

        //         if (response.status === 200 && response.data && response.data.status === 'success') {
        //             //this.$toast.success('O item está no carrinho');
        //             //window.alert('O item está no carrinho');
        //            // this.cartItems = response.data;

        //             //this.dialogCheckItemCart = true;
        //             console.log('Resposta da API:', response.data);
        //         } else {
        //             window.alert('O item não está no carrinho');
        //         }
        //     }
        //     catch(error){
        //         if(error.response){
        //             window.alert('item não encontrado no carrinho:', error.response.data);
        //           //  this.$toast.error('Erro ao verificar item no carrinho');
        //         }
        //         else{
        //             console.log('Erro desconhecido:', error);
        //             this.$toast.error('Erro desconhecido');
        //         }
        //     }
        // },
        // async pdfTag(item){
        //     try{
        //         const response = await api.post('melhorEnvio/pdfTag',{
        //             melhorenvio_id: item.melhorenvio_id
        //         });

        //         if(response.data && response.data.status == 'success'){
        //             window.alert('Etiqueta paga com sucesso');
        //         }
        //         else{
        //             window.alert('Erro ao pagar a etiqueta');
        //         }
        //     }
        //     catch(error){
        //         console.log('Erro ao pagar a etiqueta:', error);
        //         // this.$toast.error('Erro ao pagar a etiqueta');
        //     }
        // },
        // async deleteItemCart(item) {
        //     console.log(item);
        //   try{
        //     const response = await api.delete('melhorEnvio/deleteItemCart',{
        //         data: {melhorenvio_id: item.melhorenvio_id}
        //     });
        //     console.log(response)
        //     if(response.data && response.data.status == 'success' || response.status == 204){
        //         window.alert('Item deletado com sucesso');
        //         this.cartItems = this.cartItems.filter(cartItem => cartItem.id !== item.id);
        //     }
        //     else{
        //         window.alert('Erro ao deletar o item');
        //     }
        //   }
        //   catch(error){
        //     if(error.response){
        //             window.alert('item não encontrado no carrinho:', error.response.data);
        //           //  this.$toast.error('Erro ao verificar item no carrinho');
        //         }
        //         else{
        //             console.log('Erro desconhecido:', error);
        //          //   this.$toast.error('Erro desconhecido');
        //         }
        //   }
        // },
    }
};
</script>
