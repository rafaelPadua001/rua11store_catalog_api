<template>
    <v-row justify="center">
        <v-col cols="12" md="8" lg="8" xl="6">
            <v-card class="pa-4">
                <v-card-title class="d-flex justify-center">
                    <h1 class="text-h5">Payments Management</h1>
                </v-card-title>

                <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" @click="newProduct" disabled>
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions>

                <v-data-table :headers="headers" :items="payments" :items-per-page="10" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading payments...">
                    <!-- 🔹 Slot para exibir imagens -->
                    <template v-slot:item.image="{ item }">
                        <v-img v-if="item.image_path" :src="getProductImage(item.image_path, item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

                    <template v-slot:item.description="{ item }">
                        <span v-if="item.description && item.description.length > 100">
                            {{ item.description.substring(0, 38) }}...
                        </span>
                        <span v-else>
                            {{ item.description }}
                        </span>
                    </template>

                    <!-- 🔹 Slot para categoria -->
                    <template v-slot:item.category="{ item }">
                        <span v-if="item && item.category_id">{{ getCategoryName(item.category_id) }}</span>
                        <span v-else>Sem Categoria</span>
                    </template>

                    <!-- 🔹 Slot para ações -->
                    <template v-slot:item.actions="{ item }">
                        <v-icon small class="mr-2" @click.stop="openDetailsDialog(item)">
                            mdi-eye
                        </v-icon>
                        <v-icon small @click.stop="deleteProduct(item.id)">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>
            </v-card>

            <!-- Modal para Adicionar/Editar Produto -->
            <v-dialog v-model="detailsDialog" max-width="500px">
                <v-card>
                    <v-card-title class="headline">Payment #{{ selectedItem.id }}</v-card-title>

                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" class="mb-4">
                                    <b>User email:</b> {{ selectedItem.userEmail }}
                                </v-col>

                                <v-col cols="12" class="mb-4">
                                    <b>Payment ID:</b> {{ selectedItem.payment_id }}


                                    <b>Type:</b> {{ selectedItem.paymentType }}
                                </v-col>

                                <v-col cols="12" class="mb-4">
                                    <b>Method:</b> <span v-if="paymentDetails && paymentDetails.method">{{
                                        paymentDetails.method }}</span>
                                    <span v-else>-</span>
                                </v-col>

                                <v-col cols="12" class="mb-4">
                                    <b>Amount:</b>
                                    <v-text-field label="Amount" v-model="editableFields.amount" type="number"
                                        dense></v-text-field>

                                    <b>Status:</b>
                                    <v-select label="Status" v-model="editableFields.status"
                                        :items="['approved', 'rejected', 'pending', 'cancelled']" dense></v-select>

                                    <b>Created:</b>
                                    <v-text-field label="Created" v-model="editableFields.created" type="date"
                                        dense></v-text-field>

                                </v-col>



                            </v-row>
                        </v-container>


                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="grey darken-1" text @click="closeDetailsDialog">Cancel</v-btn>
                        <v-btn color="primary" text @click="updatePayment">update</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-col>
    </v-row>
</template>

<script>
import axios from "axios";


const api = axios.create({
    baseURL:
        window.location.hostname === "localhost"
            ? "http://localhost:5000"
            : "https://rua11storecatalogapi-production.up.railway.app",
    headers: { "Content-Type": "application/json" },
});

export default {
    data() {
        return {
            loading: false,
            productDialog: false,
            editedIndex: -1,
            editedPayments: null,
            detailsDialog: false,
            selectedItem: null,
            paymentDetails: null,
            editableFields: {
                amount: null,
                status: '',
                created: '',
            },
            defaultProduct: {
                id: null,
                payment_type: "",
                category_id: null,
                subcategory_id: null,
                image: null,
                description: "",
                price: 0,
                quantity: 1,
                width: 1,
                length: 1,
            },
            payments: [],
            //categories: [],
            headers: [
                { text: "ID", value: "id" },
                { text: "Payment Type", value: "paymentType" },
                { text: "Total Value", value: "totalValue", align: "right" },
                { text: "Status", value: "status" },
                { text: "Payment Date", value: "paymentDate" },
                { text: "Email", value: "userEmail" },
                { text: "User Id", value: "userId" },
                { text: "Actions", value: "actions", width: "120px", align: "center", sortable: false },
            ],

        };
    },
    watch: {
        paymentDetails: {
            handler(newVal) {
                if (newVal) {
                    this.editableFields.amount = newVal.amount;
                    this.editableFields.status = newVal.status;
                    this.editableFields.created = newVal.created?.slice(0, 10);
                } else {
                    // Opcional: zere os campos se newVal for null
                    this.editableFields.amount = null;
                    this.editableFields.status = null;
                    this.editableFields.created = null;
                }
            },
            immediate: true,
        },
    },
    computed: {
        formattedPrice: {
            get() {
                return this.editedPayments.price !== null && this.editedPayments.price !== undefined
                    ? Number(this.editedPayments.price).toFixed(2).replace(".", ",") // Garante sempre 2 casas decimais
                    : "";
            },
            set(value) {
                let numericValue = parseFloat(value.replace(/[^0-9,]/g, "").replace(",", "."));
                this.editedPayments.price = isNaN(numericValue) ? 0.00 : parseFloat(numericValue.toFixed(2)); // Mantém como número
            }
        }

    },
    created() {

        this.loadPayments();
    },
    methods: {
        async loadPayments() {
            this.loading = true;
            try {
                const response = await api.get("/payments/get-all");
                console.log(response);

                // Verificar se a resposta contém a chave 'payments' e se é um array
                if (response.data && Array.isArray(response.data.payments)) {
                    this.payments = response.data.payments.map(payment => {
                        return {
                            id: payment.id,
                            totalValue: payment.total_value,
                            paymentType: payment.payment_type,
                            payment_id: payment.payment_id,
                            status: payment.status,
                            paymentDate: payment.payment_date,
                            userEmail: payment.email,
                            //userCpf: payment.cpf,
                            userId: payment.usuario_id
                        };
                    });
                    console.log(this.payments);
                } else {
                    console.error("Resposta não contém um array de pagamentos:", response.data);
                }
            } catch (error) {
                console.error("Error loading payments:", error);
            } finally {
                this.loading = false;
            }
        },
        async openDetailsDialog(item) {
            this.selectedItem = item;
            this.detailsDialog = true;
            try {
                const response = await api.get(`/payments/payment/${item.payment_id}`)
                this.paymentDetails = response.data;
            }
            catch (error) {
                console.error("Error loading payment details:", error);
            }
        },
        closeDetailsDialog() {
            this.detailsDialog = false;
            //this.selectedItem = null;
        },
        formatDate(datetime) {
            if (!datetime) return '';

            return datetime.split('T')[0];
        },
        updatePayment() {

            let amount = this.editableFields.amount;

// Garantir que seja um valor positivo
let amountInCents = Math.abs(amount) * 100;

// Arredondar para evitar precisão excessiva
amountInCents = Math.round(amountInCents);

console.log(amountInCents);  // Agora deve ser um 
            const updatedPayment = {
                ...this.paymentDetails,
                amount: amountInCents,
                status: this.editableFields.status,
                created: this.editableFields.created,
            };

            api.put(`/payments/payment/update-status/${this.selectedItem.payment_id}`, updatedPayment)
                .then(response => {
                    console.log("Payment updated successfully:", response.data);
                    this.loadPayments();
                    this.closeDetailsDialog();
                })
                .catch(error => {
                    console.error("Error updating payment:", error);
                });
        },
    },
};
</script>