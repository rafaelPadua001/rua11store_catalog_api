<template>
    <v-row justify="center">
        <v-col>
            <v-card class="pa-4" elevation="2">
                <v-card-text>
                    <v-textarea
                        v-model="comment"
                        label="Escreva seu comentário..."
                        auto-grow
                        outlined
                        rows="2"
                        class="mb-4"
                    >

                    </v-textarea>

                    <div class="d-flex flex-column gap-3">
                        <v-checkbox
                            v-model="anonymous"
                            label="Comentar como Anônimo"
                        />

                        <div class="d-flex flex-wrap align-center">
                            <v-btn
                                color="red"
                                variant="outlined"
                                @click="login('google')"
                            >
                                <v-icon start>mdi-google</v-icon>
                                Google
                            </v-btn>
                             <v-btn
                                color="blue"
                                variant="outlined"
                                @click="login('facebook')"
                             >
                                <v-icon start>mdi-facebook</v-icon>
                                Facebook
                            </v-btn>
                             <v-btn
                                color="light-blue"
                                variant="outlined"
                                @click="login('twitter')"
                             >
                                <v-icon>mdi-twitter</v-icon>
                            </v-btn>

                           
                        </div>
                    </div>
                </v-card-text>

                <v-card-actions>
                     <div class="text-right mt-4">
                                 <v-btn
                                    color="primary"
                                    :disabled="!comment"
                                    @click="submitComment"   
                                 >
                              Enviar comentário
                            </v-btn>
                            </div>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
   
</template>

<script setup>
    import {ref} from 'vue';

    const comment = ref('');
    const anonymous = ref(false);
    const user = ref(null);

    const submitComment = () => {
        if(!comment.value) return;

        if(anonymous.value){
            console.log('Comentário anônimo:', comment.value);
        }
        else if(user.value){
            console.log('Comentário de:', comment.value)
            // chamada API -> { text: comment.value, user: user.value }
        }
        else{
            console.warn('Precisa logar ou marcar anônimo!');
        }

        console.log("commentário:", comment.value);
        console.log('Anonimo:', anonymous.value);

        //Call to api

    };

    const login = (provider) => {
        console.log('Login com:', provider);
        //Integrations here ... 

        user.value = {
            provider,
            name: "usuario teste",
            id: '12345'
        }
    }
</script>