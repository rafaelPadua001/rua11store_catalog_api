<template>
    <v-row justify="center">
        <v-col cols="12" md="8" lg="6" class="d-flex flex-column justify-center">
            <v-card rounded="xl" elevation="4">
                <!-- Toolbar -->
                <v-toolbar color="transparent">
                    <v-toolbar-title>Edit comment</v-toolbar-title>

                    <v-spacer></v-spacer>

                    <v-btn icon @click="$emit('close')">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-toolbar>

                <!-- Conteúdo -->
                <v-card-text v-if="editedComment">
                    <v-list density="compact" lines="two">
                        <v-list-item class="border-b border-gray-200">
                        
                                <div class="d-flex align-center">
                                    <!-- Avatar -->
                                    <v-avatar size="50" class="me-3">
                                        <v-img v-if="editedComment.avatar_url" :src="editedComment.avatar_url"
                                            :alt="editedComment.user_name" />
                                        <v-img v-else src="https://cdn.vuetifyjs.com/images/profiles/marcus.jpg" />
                                    </v-avatar>

                                    <!-- Nome -->
                                    <span class="font-semibold">
                                        {{ editedComment.user_name }}
                                    </span>
                                </div>
                           
                        </v-list-item>

                        <v-list-item class="border-b border-gray-200">


                            <v-textarea v-model="localComment" label="Edit your comment" rows="3" outlined />
                        </v-list-item>
                    </v-list>
                </v-card-text>

                <!-- Ações -->
                <v-divider></v-divider>
                <v-card-actions class="justify-end">
                    <v-btn variant="text" color="grey" @click="$emit('close')">Cancel</v-btn>
                    <v-btn color="primary" @click="saveEdit">Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref, watchEffect } from 'vue'


const props = defineProps({
    editedComment: {
        type: Object,
        required: true
    },
    authUser: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['save', 'close'])

// criamos uma cópia local pra editar sem alterar o original direto
const localComment = ref(props.editedComment.comment)

// se o comentário mudar no pai, sincroniza aqui
watchEffect(() => {
  if (props.editedComment) {
    localComment.value = props.editedComment.comment || ''
  }
})

const saveEdit = () => {
    
    emit('save', { ...props.editedComment, comment: localComment.value })
    emit('close');
}
</script>
