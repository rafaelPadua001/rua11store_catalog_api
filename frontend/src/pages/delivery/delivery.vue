<template>
    <v-row justify="center">
        <v-col cols="12" md="12" lg="10" xl="10" sm="12">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">Delivery Management</h1>
                </v-card-title>

                <!-- <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newProduct" disabled>
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions> -->

                <v-data-table :headers="headers" :items="deliveries" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading deliveries...">
                    <!-- Exibe imagens de produtos -->
                    <template v-slot:item.image="{ item }">
                        <v-img v-if="item.image_path" :src="getProductImage(item.image_path, item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

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
                    <template v-slot:item.category="{ item }">
                        <span v-if="item && item.category_id">{{ getCategoryName(item.category_id) }}</span>
                        <span v-else>Sem Categoria</span>
                    </template>


                    <!-- Exibe os ícones de ações -->
                    <template v-slot:item.actions="{ item }">
                         <!-- Botão de buscar item no carrinho -->
                        
                        <!-- Ícone de criar envio -->
                        <v-icon small @click.stop="shipmentCreate(item)">
                            mdi-cart
                        </v-icon>
                         <!-- Botão de compra de etiqueta no carrinho -->
                         <v-icon small @click.stop="shipmentCheckout(item)">
                            mdi-check
                        </v-icon>
                        <v-icon :disabled="!isCheckitemButton" small @click.stop="checkItemInCart(item)">
                            mdi-file-search
                        </v-icon>


                       <v-icon small @click.stop="shipmentGenerate(item)">
                            mdi-bookmark
                        </v-icon>

                        <!-- Ícone de criar etiqueta -->
                        <v-icon small @click.stop="pdfTag(item)">
                            mdi-file-pdf-box
                        </v-icon>
                        <!-- Ícone de deletar produto -->
                        <v-icon small @click.stop="deleteItemCart(item)">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>

                <v-dialog v-model="dialogCheckItemCart" max-width="600px">
                    <v-card>
                        <v-card-title>
                            <span class="headline">Detalhes da Entrega</span>
                        </v-card-title>

                       
                        <v-spacer></v-spacer>

                        <v-card-subtitle>
                            <v-row>
                                <v-col cols="8" sm="3">
                                   <strong>Id:</strong> {{ cartItems.data.id}}
                                </v-col>
                               
                            </v-row>
                            <v-row>
                                <v-col cols="8" sm="3">
                                   <strong>Order Id:</strong> {{ cartItems.data.protocol}}
                                </v-col>
                            </v-row>

                            <v-divider></v-divider>
                            <v-spacer></v-spacer>
                            
                            <v-row>
                                
                                <v-col cols="12" sm="6">
                                   <strong>Nome do Destinatário:</strong> {{ cartItems.data.to.name }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Endereço:</strong> {{ cartItems.data.to.address }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>CEP:</strong> {{ cartItems.data.to.postal_code }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Cidade:</strong> {{ cartItems.data.to.city }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Estado:</strong> {{ cartItems.data.to.state_abbr }}
                                </v-col>
                              
                                <v-col cols="12" sm="6">
                                    <strong>Telefone:</strong> {{ cartItems.data.to.phone }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Email:</strong> {{ cartItems.data.to.email }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Status:</strong>
                                    <strong v-if="cartItems.data.status == 'pending'" class="text-blue"> {{ cartItems.data.status }}</strong> 
                                    <strong v-else> {{ cartItems.data.status }}</strong> 
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Delivery max: </strong>
                                    <strong> {{ cartItems.data.delivery_max }} dias uteis</strong> 
                                    
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Format: </strong>
                                    <strong> {{ cartItems.data.format }} </strong> 
                                    
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Price: </strong>
                                    <strong> {{ cartItems.data.price }} </strong> 
                                    
                                </v-col>
                            </v-row>

                            <v-row>
                                <v-col>
                                    <v-list>
                                        <strong>Itens: ({{cartItems.data.products.length}})</strong>
                                        <v-divider></v-divider>
                                        <v-list-item 
                                            v-for="(product ,index) in cartItems.data.products"
                                            :key="index"
                                        >
                                            <v-list-item-content>
                                                <v-list-item-title>{{ product.name }}</v-list-item-title>
                                                <v-list-item-subtitle>Quantitdade: {{product.quantity}} - Preço: {{ product.unitary_value }}</v-list-item-subtitle>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-list>
                                </v-col>
                            </v-row>
                        </v-card-subtitle>

                        <v-card-actions>
                            <!-- Botão de compra de etiqueta no carrinho -->
                            
                            <v-btn color="green" text @click="dialogCheckItemCart = false">Close</v-btn>
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
            deliveries: [],
            cartItems: [],
            shipment: [],
            headers: [
                { text: "ID", value: "id" },
                { text: "User ID", value: "user_id" },
                { text: "Recipient Name", value: "recipient_name" },
                { text: "Street", value: "street", align: "right" },
                { text: "number", value: "number" },
                { text: "complement", value: "complement" },
                { text: "city", value: "city" },
                { text: "state", value: "state" },
                { text: "zipcode", value: "zip_code" },
                { text: "bairro", value: "bairro" },
                { text: "country", value: "country" },
                { text: "phone", value: "phone" },
                { text: "Email", value: "userEmail" },
                { text: "Price", value: "price" },
                // { text: "Delivery", value: "delivery_id" },
                { text: "Actions", value: "actions", width: "120px", align: "center", sortable: false },
            ],
            isPaymentButtonPayTagDisabled: true,
            isCheckitemButton: true,
            dialogCheckItemCart: false,
        };
    },
    computed: {
        formattedPrice: {
            get() {
                return this.editedDeliveries && this.editedDeliveries.price !== undefined
                    ? Number(this.editedDeliveries.price).toFixed(2).replace(".", ",")
                    : "";
            },
            set(value) {
                let numericValue = parseFloat(value.replace(/[^0-9,]/g, "").replace(",", "."));
                this.editedDeliveries.price = isNaN(numericValue) ? 0.00 : numericValue;
            }
        }
    },
    created() {
        this.loadDeliveries();
    },
    methods: {
        async loadDeliveries() {
            this.loading = true;
            try {
                const response = await api.get("delivery/deliveries");
                if (response.data && Array.isArray(response.data)) {
                    this.deliveries = response.data.flat().map(delivery => ({
                        id: delivery.id,
                        recipient_name: delivery.recipient_name,
                        street: delivery.street,
                        number: delivery.number,
                        complement: delivery.complement,
                        city: delivery.city,
                        state: delivery.state,
                        zip_code: delivery.zip_code.replace(/\D/g, ''),
                        bairro: delivery.bairro,
                        country: delivery.country,
                        phone: delivery.phone,
                        price: delivery.total_value,
                        delivery_id: delivery.delivery_id,
                        email: delivery.email,
                        products: delivery.products,
                        height: delivery.height,
                        width: delivery.width,
                        length: delivery.length,
                        weight: delivery.weight,
                        cpf: delivery.cpf.replace(/\D/g, ''),
                        melhorenvio_id: delivery.melhorenvio_id,
                        order_id: delivery.order_id
                        //   email: delivery.userEmail,

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
        async shipmentCreate(item) {
            try {
                const response = await api.post('/melhorEnvio/shipmentCreate', item);

                // Exibindo a resposta no console. Normalmente, a resposta está em response.data
                console.log('Resposta da API:', response.data); // Isso é geralmente a parte importante

                if (response.data.message == 'Envio criado com sucesso. Aguarde pagamento.') {
                    this.isPaymentButtonPayTagDisabled = false;
                    this.isCheckitemButton = true;
                    // this.$toast.success('Etiqueta enviada com sucesso');
                    this.shipment.push(response.data.shipment);
                    console.log(this.shipment);
                    window.alert('Envio criado com sucesso')
                }
                else {
                    window.alert('Algo deu errado. Por favor, tente novamente.');
                    //this.$toast.error('Algo deu errado. Por favor, tente novamente.');
                }
                // Exibe uma mensagem de sucesso
                console.log('success');
                //this.$toast.success('Etiqueta enviada com sucesso');

            } catch (error) {
                console.log('Erro no envio:', error);
                //   this.$toast.error('Erro ao enviar os dados para o backend');
            }
        },
        async checkItemInCart(item) {
            try {
                const response = await api.post(`/melhorEnvio/checkItemInCart/${item.id}`, {
                    melhorenvio_id: item.melhorenvio_id,
                    order_id: item.order_id
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                if (response.status === 200 && response.data && response.data.status === 'success') {
                    // this.$toast.success('O item está no carrinho');
                    //window.alert('O item está no carrinho');
                    this.cartItems = response.data;
                    this.shipment.push(this.cartItems);
                    this.dialogCheckItemCart = true;
                } else {
                    this.$toast.info('O item não está no carrinho');
                }

            } catch (error) {
                // Verifique se o erro contém a propriedade response
                if (error.response) {
                    window.alert('item não encontrado no carrinho:', error.response.data);
                   // this.$toast.error('Erro ao verificar item no carrinho');
                } else {
                    // Se não houver response, logue o erro simples
                    console.log('Erro desconhecido:', error);
                   // this.$toast.error('Erro desconhecido');
                }
            }
        },
        async shipmentCheckout(item) {
            console.log(item);
            try {
                const response = await api.post(`/melhorEnvio/shipmentCheckout`, {
                    item: item
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.status === 200 && response.data && response.data.status === 'success') {
                    // this.$toast.success('O item está no carrinho');
                    //window.alert('O item está no carrinho');
                    this.cartItems = response.data;

                    this.dialogCheckItemCart = true;
                } else {
                    //this.$toast.info('O item não está no carrinho');
                    window.alert('O item não está no carrinho');
                }

            } catch (error) {
                // Verifique se o erro contém a propriedade response
                if (error.response) {
                    window.alert('item não encontrado no carrinho:', error.response.data);
                  //  this.$toast.error('Erro ao verificar item no carrinho');
                } else {
                    // Se não houver response, logue o erro simples
                    console.log('Erro desconhecido:', error);
                    // this.$toast.error('Erro desconhecido');
                }
            }
        },
        async shipmentGenerate(item) {
            console.log(item);
            try {
                const response = await api.post(`/melhorEnvio/shipmentGenerate`, {
                    melhorenvio_id: item.melhorenvio_id
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.status === 200 && response.data && response.data.status === 'success') {
                    //this.$toast.success('O item está no carrinho');
                    //window.alert('O item está no carrinho');
                    // this.cartItems = response.data;

                    //this.dialogCheckItemCart = true;
                    console.log('Resposta da API:', response.data);
                } else {
                    window.alert('O item não está no carrinho');
                }
            }
            catch (error) {
                if (error.response) {
                    window.alert('item não encontrado no carrinho:', error.response.data);
                    //  this.$toast.error('Erro ao verificar item no carrinho');
                }
                else {
                    console.log('Erro desconhecido:', error);
                    this.$toast.error('Erro desconhecido');
                }
            }
        },
        async pdfTag(item) {
            try {
                const response = await api.post('melhorEnvio/pdfTag', {
                    melhorenvio_id: item.melhorenvio_id
                });

                if (response.data && response.data.status == 'success') {
                    window.alert('Etiqueta paga com sucesso');
                }
                else {
                    window.alert('Erro ao pagar a etiqueta');
                }
            }
            catch (error) {
                console.log('Erro ao pagar a etiqueta:', error);
                // this.$toast.error('Erro ao pagar a etiqueta');
            }
        },
        async deleteItemCart(item) {
            console.log(item);
            try {
                const response = await api.delete('melhorEnvio/deleteItemCart', {
                    data: { melhorenvio_id: item.melhorenvio_id }
                });
                console.log(response)
                if (response.data && response.data.status == 'success' || response.status == 204) {
                    window.alert('Item deletado com sucesso');
                    this.cartItems = this.cartItems.filter(cartItem => cartItem.id !== item.id);
                }
                else {
                    window.alert('Erro ao deletar o item');
                }
            }
            catch (error) {
                if (error.response) {
                    window.alert('item não encontrado no carrinho:', error.response.data);
                    //  this.$toast.error('Erro ao verificar item no carrinho');
                }
                else {
                    console.log('Erro desconhecido:', error);
                    //   this.$toast.error('Erro desconhecido');
                }
            }
        },
    }
};
</script>
