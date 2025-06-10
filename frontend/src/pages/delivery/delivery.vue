<template>
    <v-row justify="center">
        <v-col cols="12" md="12" lg="12" xl="12">
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

                  


                    <!-- Exibe os ícones de ações -->
                    <template v-slot:item.actions="{ item }">
                        <!-- Botão de buscar item no carrinho -->

                        <!-- Ícone de criar envio -->
                        <v-icon small @click.stop="shipmentCreate(item)">
                            mdi-cart
                        </v-icon>


                        <v-icon :disabled="!isCheckitemButton" small @click.stop="checkItemInCart(item)">
                            mdi-file-search
                        </v-icon>

                        <!-- Botão de compra de etiqueta no carrinho -->
                        <v-icon small @click.stop="shipmentCheckout(item)">
                            mdi-check
                        </v-icon>
                        <v-icon small @click.stop="shipmentGenerate(item)">
                            mdi-bookmark
                        </v-icon>
                        <v-icon small @click.stop="shipmentPrint(item)">
                            mdi-file-pdf-box
                        </v-icon>


                        <!-- Ícone de criar etiqueta -->
                        <!-- <v-icon small @click.stop="pdfTag(item)">
                            mdi-file-pdf-box
                        </v-icon> -->
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
                                    <strong>Id:</strong> {{ cartItems.data.id }}
                                </v-col>

                            </v-row>
                            <v-row>
                                <v-col cols="8" sm="3">
                                    <strong>Order Id:</strong> {{ cartItems.data.protocol }}
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
                                    <strong v-if="cartItems.data.status == 'pending'" class="text-blue"> {{
                                        cartItems.data.status
                                        }}</strong>
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
                                        <strong>Itens: ({{ cartItems.data.products.length }})</strong>
                                        <v-divider></v-divider>
                                        <v-list-item v-for="(product, index) in cartItems.data.products" :key="index">
                                            <v-list-item-content>
                                                <v-list-item-title>{{ product.name }}</v-list-item-title>
                                                <v-list-item-subtitle>Quantitdade: {{ product.quantity }} - Preço: {{
                                                    product.unitary_value }}</v-list-item-subtitle>
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
        : "https://rua11store-catalog-api-lbp7.onrender.com",
    headers: { "Content-Type": "application/json" },
});

export default {
    data() {
        return {
            loading: false,
            deliveries: [],
            cartItems: [],
            checkItemEnabled: {},
            shipment: [],
            headers: [
                { title: "ID", key:"id" },
                { title: "User ID", key:"user_id" },
                { title: "Recipient Name", key:"recipient_name" },
                { title: "Street", key: "street", align: "right" },
                { title: "Number", key: "number" },
                { title: "Complement", key: "complement" },
                { title: "City", key: "city" },
                { title: "State", key: "state" },
                { title: "Postal Code", key: "zip_code" },
                { title: "Bairro", key: "bairro" },
                { title: "Country", key: "country" },
                { title: "Phone", key: "phone" },
                { title: "Email", key: "email" },
                { title: "Price", key: "price" },
                { title: "Status", key:"status" },
                // { title: "Delivery", key: "delivery_id" },
                { title: "Actions", key: "actions", width: "120px", align: "center", sortable: false },
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
                        order_id: delivery.order_id,
                        user_id: delivery.user_id,
                        status: delivery.status,
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
        console.log('Resposta da API:', response.data);

        if (response.data.message === 'Envio criado com sucesso. Aguarde pagamento.') {
            const shipmentId = response.data.shipment_id;

            // Forçando reatividade (Vue 2)
          item.melhorenvio_id = shipmentId;


            this.isPaymentButtonPayTagDisabled = false;
            this.isCheckitemButton = true;
            
            // Atualizando a lista de envios, se necessário
           this.shipment = [...this.shipment];


            // Nenhum reload necessário
            return window.alert('item adicionado ao carrinho do melhor envio');
        } else {
            window.alert('Algo deu errado. Por favor, tente novamente.');
        }
    } catch (error) {
        console.log('Erro no envio:', error);
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
                    this.dialogCheckItemCart = true;
                    return this.shipment.push(this.cartItems);
                    
                } else {
                    // this.$toast.info('O item não está no carrinho');
                    window.alert('O item não está no carrinho');
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
                    window.alert('O item está no carrinho');
                    this.dialogCheckItemCart = true;
                    return this.cartItems.push(response.data);
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
        async shipmentPrint(item) {
            try {
                const response = await api.post(`/melhorEnvio/shipmentPrint`, {
                    melhorenvio_id: item.melhorenvio_id
                }, {
                    headers: { 'Content-Type': 'application/json' }
                });

                if (response.status === 200) {
                    const urlEtiqueta = response.data.url;  // pega a URL da etiqueta da resposta
                    if (urlEtiqueta) {
                        // Abre a etiqueta em nova aba
                        window.open(urlEtiqueta, '_blank');
                    } else if (response.data.error) {
                        window.alert('Erro: ' + response.data.error);
                    } else {
                        window.alert('Etiqueta não disponível');
                    }
                } else {
                    window.alert('Falha ao gerar etiqueta');
                }
            } catch (error) {
                if (error.response && error.response.data) {
                    window.alert('Erro: ' + (error.response.data.error || 'Erro desconhecido'));
                } else {
                    window.alert('Erro desconhecido');
                    console.error(error);
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

                if (response.status === 200 || response.status === 204 || response.status == true) {
                    //this.$toast.success('O item está no carrinho');
                    window.alert('O item está no carrinho');
                    return this.cartItems.push(response.data);

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
                const response = await api.post('melhorEnvio/pdfTag',
                    { melhorenvio_id: item.order_id },
                    { headers: { 'Content-Type': 'application/json' } }
                );
                console.log('Resposta da API:', response.data);

                const pdfUrls = response.data; // isso deve ser um array
                if (pdfUrls && pdfUrls.length > 0) {
                    const pdfUrl = pdfUrls[0];
                    console.log('URL do PDF:', pdfUrl);

                    window.open(pdfUrl, '_blank'); // abre em nova aba
                } else {
                    window.alert('Nenhuma URL de PDF recebida.');
                }
            } catch (error) {
                window.alert('Erro ao buscar PDF: ' + error);
            }
        },

        async deleteItemCart(item) {
           
            try {
                const response = await api.delete('melhorEnvio/deleteItemCart', {
                    data: { melhorenvio_id: item.melhorenvio_id }
                });
                console.log(response)
                if ((response.data && response.data.status == 'success') || response.status == 204) {
                    window.alert('Item deletado com sucesso');
                    return this.cartItems = this.cartItems.filter(cartItem => cartItem.melhorenvio_id !== item.melhorenvio_id);
                }
                else {
                    window.alert('Erro ao deletar o item');
                }
            }
            catch (error) {
                if (error.response) {
                     if (error.response.status === 404) {
            window.alert('Item já não estava no carrinho (404). Atualizando lista local.');
            this.cartItems = this.cartItems.filter(cartItem => cartItem.melhorenvio_id !== item.melhorenvio_id);
        } else {
            window.alert('Erro ao deletar o item:', error.response.data);
        }
                  
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
