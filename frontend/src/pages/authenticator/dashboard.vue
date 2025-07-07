<template>
    <v-container fluid>
        <v-row>
            <v-col cols="12">
                <v-card class="pa-4 mb-4">
                    <v-row align="center">
                        <v-col cols="auto">
                            <v-icon color="primary" size="36">
                                <v-avatar size="48">
                                    <v-img
                                        src="https://imgs.search.brave.com/Zsapxs7JqY0v8BYpGwgMnI1WLK_J9l-O1IMIOUuzTGc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9waWNz/LmNyYWl5b24uY29t/LzIwMjQtMDktMDcv/djc1XzNnV0VUTWVL/UHJmWmFXWlFKQS53/ZWJw" />
                                </v-avatar></v-icon>
                        </v-col>
                        <v-col>
                            <div class="text-h5 font-weight-bold">Bem-vindo de volta, Usuário!</div>
                            <div class="text-subtitle-2">{{ dateToday }}</div>
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>

        <!-- Cads Resumo-->
        <v-row>
            <v-col cols="12" sm="4">
                <v-card class="pa-4">
                    <v-card-title>Carrinhos Ativos</v-card-title>
                    <v-card-text class="text-h5 font-weight-bold">0</v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12" sm="4">
                <v-card class="pa-4">
                    <v-card-title>Pedidos de Hoje</v-card-title>
                    <v-card-text class="text-h5 font-weight-bold">0</v-card-text>
                </v-card>
            </v-col>
            

            <v-col cols="12" sm=4>
                <v-card class="pa-3">
                    <v-card-title>Receita de Hoje</v-card-title>
                    <v-card-text class="text-h5 font-weight-bold">R$ 0.00</v-card-text>
                </v-card>
            </v-col>
             
        </v-row>

        <v-row>
            <v-col cols="12" sm="4">
                <v-card>
                    <v-card-title>Produtos Mais Pedidos</v-card-title>
                    <v-card-title class="text-h5 font-weight-bold">Mais pedidos aqui...</v-card-title>
                </v-card>
            </v-col>
            <v-col cols="12" sm="4">
                <v-card>
                    <v-card-title>Fora do Estoque</v-card-title>
                    <v-card-title class="text-h5 font-weight-bold">Produtos fora do estoque aqui...</v-card-title>
                </v-card>
            </v-col>
        </v-row>

         

        <!-- Seção futura para grafico ou tabela -->
        <v-row>
            <v-col cols="12">
                <v-card class="pa-4">
                    <v-card-title>Vendas nos ultimos 7 dias</v-card-title>
                    <v-card-text>
                        <p>Gráfico de exemplo...</p>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>

</template>

<script>
export default {
    data() {
        return {
            dateToday: this.capitalizeFirstLetter(
                new Date().toLocaleDateString('pt-BR', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                })
            ),
        };
    },
    methods: {
        capitalizeFirstLetter(text) {
            return text.charAt(0).toUpperCase() + text.slice(1);
        },
    }

};
</script>