<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" md="10" lg="10" xl="6" sm="12">
            <v-card class="pa-4" elevation="0">
                <v-card-title class="d-flex justify-center">
                    <h5>Delivery Management</h5>
                </v-card-title>
                <v-divider></v-divider>

                <v-data-table :headers="headers" :items="deliveries" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading deliveries...">

                    <!-- Exibe imagens de produtos -->
                    <template v-slot:item.thumbnail_path="{ item }">
                        <v-img v-if="item.thumbnail_path" :src="getProductImage(item.thumbail_path, item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

                    <template v-slot:item.price="{ item }">
                        <span v-if="item.price">R$ {{ item.price.toFixed(2) }}</span>
                        <span v-else>no value found...</span>
                    </template>

                    <template v-slot:item.status="{ item }">
                        <span v-if="item.status == 'created' || item.status == 'printed'">
                            <v-chip color="success">{{ item.status }}</v-chip>
                        </span>
                        <span v-else-if="item.status == 'updated' || item.status == 'pending'">
                            <v-chip color="primary">{{ item.status }}</v-chip>
                        </span>
                        <span v-else-if="item.status == 'deleted' || item.status == 'canceled'">
                            <v-chip color="error">{{ item.status }}</v-chip>
                        </span>
                        <span v-else-if="item.status == 'purchased'">
                            <v-chip color="warning">{{ item.status }}</v-chip>
                        </span>

                    </template>
                    <!-- Exibe os ícones de ações -->
                    <template v-slot:item.actions="{ item }">

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
                        <v-divider></v-divider>

                        <v-spacer></v-spacer>

                        <v-card-subtitle>
                            <v-row>
                                <!--<v-col cols="12" sm="6">
      <strong>ID:</strong> {{ delivery.id }}
    </v-col> -->
                                <v-col cols="12" sm="6">
                                    <strong>Destinatário:</strong> {{ delivery.recipient_name }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Usuário:</strong> {{ delivery.user_name }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Rua:</strong> {{ delivery.street }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Número:</strong> {{ delivery.number }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Complemento:</strong> {{ delivery.complement }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Cidade:</strong> {{ delivery.city }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Estado:</strong> {{ delivery.state }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>CEP:</strong> {{ delivery.zip_code }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Bairro:</strong> {{ delivery.bairro }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>País:</strong> {{ delivery.country }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Telefone:</strong> {{ delivery.phone }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Email:</strong> {{ delivery.email }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Status:</strong> {{ delivery.status }}
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Delivery Min:</strong> {{ delivery.delivery_min }} days
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Delivery Max:</strong> {{ delivery.delivery_max }} days
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <strong>Tracking code:</strong> {{ delivery.tracking }}
                                </v-col>
                            </v-row>

                            <v-divider></v-divider>
                            <div v-if="cartItems && cartItems.data && cartItems.data.products && cartItems.data.products.length">

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
                                            <v-list-item v-for="(product, index) in cartItems.data.products"
                                                :key="index">
                                                <v-list-item-title>{{ product.name }}</v-list-item-title>
                                                <v-list-item-subtitle>Quantitdade: {{ product.quantity }} - Preço: {{
                                                    product.unitary_value }}</v-list-item-subtitle>
                                            </v-list-item>
                                        </v-list>
                                    </v-col>
                                </v-row>
                            </div>
                           <div v-else-if="this.loadingCart">
                                <v-progress-circular indeterminate color="primary" />
                            </div>

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
import { toRaw } from 'vue';

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
            delivery: [],
            deliveries: [],
            cartItems: [],
            checkItemEnabled: {},
            shipment: [],
            headers: [
                { title: "ID", key: "id" },
                // { title: "User ID", key: "user_id" },
                { title: "Status", key: "status" },
                { title: "Payer Name", key: "user_name" },
                { title: "Payer Email", key: "email" },
                //{ title: "Recipient Name", key: "recipient_name" },
                // { title: "Street", key: "street", align: "right" },
                // { title: "Number", key: "number" },
                // { title: "Complement", key: "complement" },
                // { title: "City", key: "city" },
                //   { title: "State", key: "state" },
                //   { title: "Postal Code", key: "zip_code" },
                //    { title: "Bairro", key: "bairro" },
                //   { title: "Country", key: "country" },
                //   { title: "Phone", key: "phone" },
                { title: "Price", key: "price" },

                // { title: "Delivery", key: "delivery_id" },
                { title: "Actions", key: "actions", width: "100px", align: "center", sortable: false },
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
                // console.log(response.data);
                if (response.data && Array.isArray(response.data)) {
                    this.deliveries = response.data.flat().map(delivery => {
                        // Extrair todos os produtos de todos os orders da entrega
                        let allProducts = [];
                        if (delivery.orders && Array.isArray(delivery.orders)) {
                            delivery.orders.forEach(order => {
                                if (order.products && Array.isArray(order.products)) {
                                    allProducts = allProducts.concat(order.products);
                                }
                            });
                        }

                        return {
                            id: delivery.id,
                            recipient_name: delivery.recipient_name,
                            user_name: delivery.user_name,
                            street: delivery.street,
                            number: delivery.number,
                            complement: delivery.complement,
                            city: delivery.city,
                            state: delivery.state,
                            zip_code: delivery.zip_code ? delivery.zip_code.replace(/\D/g, '') : '',
                            bairro: delivery.bairro,
                            country: delivery.country,
                            phone: delivery.phone,
                            price: delivery.total_value,
                            delivery_id: delivery.delivery_id,
                            email: delivery.email,
                            products: allProducts,  // produtos agrupados de todos os orders
                            height: delivery.height,
                            width: delivery.width,
                            length: delivery.length,
                            weight: delivery.weight,
                            cpf: delivery.cpf,
                            melhorenvio_id: delivery.melhorenvio_id,
                            order_id: delivery.order_id,
                            user_id: delivery.user_id,
                            status: delivery.status,
                            delivery_min: delivery.delivery_min,
                            delivery_max: delivery.delivery_max,
                            tracking: delivery.tracking,
                        };
                    });

                    //  console.log(response.data);
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
                // console.log('Item antes:', toRaw(item.products));  // mostra o array puro de produtos

                let allProducts = [];

                if (item.products && item.products.length > 0) {
                    item.products.forEach(product => {
                        if (
                            product.name &&
                            typeof product.price === 'number' &&
                            typeof product.quantity === 'number'
                        ) {
                            allProducts.push({
                                name: product.name,
                                price: product.price,
                                quantity: product.quantity
                            });
                        } else {
                            console.warn('Produto inválido ignorado:', product);
                        }
                    });
                }

                if (allProducts.length === 0) {
                    return window.alert('Erro: Nenhum produto com name, price e quantity válido encontrado.');
                }

                item.products = allProducts;

                //console.log('Payload final antes do envio:', toRaw(item));

                const response = await api.post('/melhorEnvio/shipmentCreate', item);

                if (response.data.message === 'Envio criado com sucesso. Aguarde pagamento.') {
                    item.melhorenvio_id = response.data.shipment_id;

                    this.isPaymentButtonPayTagDisabled = false;
                    this.isCheckitemButton = true;

                    window.alert('Item adicionado ao carrinho do Melhor Envio');
                } else {
                    window.alert('Algo deu errado. Por favor, tente novamente.');
                }
            } catch (error) {
                console.error('Erro ao criar envio:', error.response?.data || error.message || error);
                window.alert('Erro ao criar envio. Detalhes no console.');
            }
        },
        async checkItemInCart(item) {
            this.delivery = item;
            this.cartItems = { data: { products: [] } }; // inicializa para evitar erro
            this.loadingCart = true;
            this.dialogCheckItemCart = true;

            try {
                const response = await api.post(`/melhorEnvio/checkItemInCart/${item.id}`, {
                    melhorenvio_id: item.melhorenvio_id,
                    order_id: item.order_id
                });

                if (response.status === 200 && response.data && response.data.status === 'success') {
                    this.cartItems = response.data;
                    this.shipment.push(this.cartItems); // se necessário
                } else {
                    window.alert('O item não está no carrinho');
                }
            } catch (error) {
                if (error.response) {
                    console.log('Item não encontrado no carrinho: ' + JSON.stringify(error.response.data));
                } else {
                    console.log('Erro desconhecido:', error);
                }
            } finally {
                this.loadingCart = false;
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
