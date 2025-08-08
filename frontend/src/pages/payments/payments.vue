<template>
    <v-row justify="center" no-gutters>
        <v-col cols="12" sm="12" md="10" lg="10" xl="6">
            <v-card class="pa-4" elevation="0">
                <v-card-title class="d-flex justify-center" elevation="0">
                    <h5>Payments Management</h5>
                </v-card-title>
                <v-divider></v-divider>

               <!-- <v-card-actions class="d-flex justify-end mb-4">
                    <v-btn color="primary" disabled>
                        <v-icon left>mdi-plus</v-icon>
                        Add Product
                    </v-btn>
                </v-card-actions> -->

                <v-data-table :headers="headers" :items="payments" :items-per-page="20" class="elevation-1"
                    item-key="id" fixed-header height="500" :loading="loading" loading-text="Loading payments...">
                    <!-- 🔹 Slot para exibir imagens -->
                    <template v-slot:item.image="{ item }">
                        <v-img v-if="item.image_path" :src="getProductImage(item.image_path, item.id)"
                            alt="Imagem do Produto" contain min-width="60" max-width="70" min-height="10"
                            class="rounded-lg"></v-img>
                        <span v-else>Sem Imagem</span>
                    </template>

                    <template v-slot:item.totalValue="{ item }">
                        <span v-if="item.totalValue">
                            R$ {{ item.totalValue }}
                        </span>
                        <span v-else>
                            R$ {{ item.totalValue }}
                        </span>
                    </template>

                    <template v-slot:item.status="{item}">
                        <span v-if="item.status === 'pending'">
                            <v-chip color="primary">
                                {{ item.status }}
                            </v-chip>
                        </span>
                         <span v-else-if="item.status === 'approved'">
                            <v-chip color="success">
                                {{ item.status }}
                            </v-chip>
                        </span>
                         <span v-else-if="item.status === 'rejected'">
                            <v-chip color="error">
                                {{ item.status }}
                            </v-chip>
                        </span>
                    </template>

                    <template v-slot:item.paymentDate="{item}">
                        {{ new Date(item.paymentDate).toLocaleDateString('pt-BR')  }}
                    </template>


                    <!-- 🔹 Slot para ações -->
                    <template v-slot:item.actions="{ item }">
                        <v-icon small class="mr-2" @click.stop="openDetailsDialog(item)" color="primary">
                            mdi-eye
                        </v-icon>
                        <v-icon small @click.stop="deleteProduct(item.id)" color="error">
                            mdi-delete
                        </v-icon>
                    </template>
                </v-data-table>
            </v-card>

            <!-- Modal para Adicionar/Editar Produto -->
            <v-dialog v-model="detailsDialog" max-width="800px">
                <v-card>
                    <v-card-title class="headline">Payment #{{ selectedItem.id }}</v-card-title>

                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" sm="6" class="mb-4">
                                    <b>Payment Id:</b> #{{ selectedItem.paymentId }}
                                </v-col>
                                <v-col cols="12" sm="6" class="mb-4">
                                    <b>Type:</b> {{ selectedItem.paymentType }}
                                </v-col>
                                <v-col cols="12" sm="6" class="mb-4">
                                    <b>User CPF:</b> {{ maskCpf(selectedItem.userCpf) }}
                                </v-col>
                                <v-col cols="12" sm="6" class="mb-4">
                                    <b>User Name:</b> {{ selectedItem.userName }}
                                </v-col>

                                <v-col cols="12" sm="6" class="mb-4">
                                    <b>User email:</b> {{ selectedItem.userEmail }}
                                </v-col>

                                <v-col cols="12" sm="6" class="mb-4">
                                    <b>Method:</b> <span v-if="paymentDetails && paymentDetails.method">{{
                                        paymentDetails.method }}</span>
                                    <span v-else>-</span>
                                </v-col>

                                <v-col cols="12" sm="6" class="mb-4">
                                    <b>Coupon code:</b> <span v-if="paymentDetails && paymentDetails.coupon_code">{{
                                        paymentDetails.coupon_code }}</span>
                                    <span v-else>-</span>
                                </v-col>

                                <v-col cols="12" sm="6" class="mb-4">
                                    <b>Coupon amount:</b> <span v-if="paymentDetails && paymentDetails.coupon_amount">{{
                                        paymentDetails.coupon_amount }}</span>
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
                        <v-btn color="primary" text @click="updatePayment">update</v-btn>
                        <v-btn color="primary" text @click="chargebackPayment">chargeback</v-btn>
                        <v-btn color="primary" text @click="refundPayment">refund</v-btn>
                        <v-btn color="grey darken-1" text @click="closeDetailsDialog">Cancel</v-btn>
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
            : "https://rua11store-catalog-api-lbp7.onrender.com",
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

            payments: [],
            //categories: [],
            headers: [
                { title: "Id", key: "id" },
                { title: "Name", key: "userName" },
                { title: "Email", key: "userEmail" },
                // { title: "Payment Id", key: "paymentId" },
                //{ title: "Payment Type", key: "paymentType" },
                { title: "Status", key: "status" },
                // { title: "User Id", key: "userId" },
                { title: "Total Value", key: "totalValue", align: "end" },
                { title: "Payment Date", key: "paymentDate" },
                { title: "Actions", key: "actions", width: "100px", align: "center", sortable: false },
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
                return this.editedPayments.totalValue !== null && this.editedPayments.totalValue !== undefined
                    ? Number(this.editedPayments.price).toFixed(2).replace(".", ",") // Garante sempre 2 casas decimais
                    : "";
            },
            set(value) {
                let numericValue = parseFloat(value.replace(/[^0-9,]/g, "").replace(",", "."));
                this.editedPayments.totalValue = isNaN(numericValue) ? 0.00 : parseFloat(numericValue.toFixed(2)); // Mantém como número
            }
        }

    },
    created() {

        this.loadPayments();
    },
    methods: {
        async loadPayments() {
            this.loading = true;
            api.get("/payments/get-all")
                .then((response) => {
                    if (response.data && response.data.payments) {
                        this.payments = response.data.payments.map((payment, index) => ({
                            id: payment.id,
                            paymentId: payment.payment_id,
                            paymentType: payment.payment_type,
                            totalValue: payment.total_value,
                            status: payment.status,
                            paymentDate: payment.payment_date,
                            userEmail: payment.email,
                            userName: payment.name,
                            userId: payment.usuario_id,
                            userCpf: payment.cpf
                        }));
                    } else {
                        this.payments = [];
                    }
                })
                .catch((error) => {
                    console.error("Erro ao carregar pagamentos:", error);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        maskCpf(cpf) {
            if (!cpf) return '';
            const strCpf = cpf.toString();

            return '***.***.***-' + strCpf.slice(-3);

        },
        async openDetailsDialog(item) {
            this.selectedItem = item;
            this.detailsDialog = true;
            try {
                const response = await api.get(`/payments/payment/${this.selectedItem.paymentId}`)
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

            api.put(`/payments/payment/update-status/${this.selectedItem.paymentId}`, updatedPayment)
                .then(response => {
                    console.log("Payment updated successfully:", response.data);
                    this.loadPayments();
                    this.closeDetailsDialog();
                })
                .catch(error => {
                    console.error("Error updating payment:", error);
                });
        },
        chargebackPayment() {
            api.post(`/payments/payment/chargeback/${this.selectedItem.paymentId}`)
                .then(response => {
                    console.log("Chargeback successful:", response.data);
                    this.loadPayments();
                    this.closeDetailsDialog();
                })
                .catch(error => {
                    console.error("Error processing chargeback:", error);
                });
        },
        refundPayment() {
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
            api.post(`/payments/payment/refund/${this.selectedItem.paymentId}`, updatedPayment)
                .then(response => {
                    this.loadPayments();
                    this.closeDetailsDialog();
                })
                .catch(error => {
                    console.error("Error processing chargeback:", error);
                });
        },
    },
};
</script>