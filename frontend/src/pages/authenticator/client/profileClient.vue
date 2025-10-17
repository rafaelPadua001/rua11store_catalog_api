<template>
  <v-container class="py-6">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-6" elevation="2" rounded="xl">
          <!-- Cabeçalho do perfil -->
          <v-row align="center" class="mb-6">
            <v-col cols="12" md="4" class="d-flex justify-center">
              <v-avatar size="120">
                <v-img
                  src="https://cdn.vuetifyjs.com/images/john.jpg"
                  alt="User Avatar"
                ></v-img>
              </v-avatar>
            </v-col>
            <v-col cols="12" md="8" class="text-center text-md-left">
              <h2 class="font-weight-bold mb-1">Marcos Obrien</h2>
              <p class="text-medium-emphasis mb-1">Network Engineer</p>
              <p class="text-caption">marcos.obrien@example.com</p>
              <v-btn color="primary" variant="flat" size="small" class="mt-2">
                Edit Profile
              </v-btn>
            </v-col>
          </v-row>

          <v-divider class="mb-4"></v-divider>

          <!-- Bio -->
          <h3 class="text-subtitle-1 font-weight-medium mb-2">About</h3>
          <p class="text-body-2 mb-6">
            Passionate network engineer with 8 years of experience in data
            security and infrastructure management. Loves technology,
            photography, and exploring new coffee places.
          </p>

          <!-- Informações extras -->
          <v-row dense>
            <v-col cols="12" sm="6">
              <v-card class="pa-3" variant="outlined" rounded="lg">
                <v-icon class="mr-2" color="blue">mdi-map-marker</v-icon>
                <span>São Paulo, Brazil</span>
              </v-card>
            </v-col>
            <v-col cols="12" sm="6">
              <v-card class="pa-3" variant="outlined" rounded="lg">
                <v-icon class="mr-2" color="green">mdi-calendar</v-icon>
                <span>Joined: March 2022</span>
              </v-card>
            </v-col>
          </v-row>

          <!-- Sessão inferior: pedidos, atividades, etc -->
          <h3 class="text-subtitle-1 font-weight-medium mt-6 mb-3">
            Recent Activity
          </h3>
          <v-list density="compact" lines="two">
            <v-list-item
              prepend-icon="mdi-cart"
              title="Order #1024"
              subtitle="Placed 3 days ago"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-message"
              title="Commented on 'Network Setup Guide'"
              subtitle="2 days ago"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-account-edit"
              title="Updated profile info"
              subtitle="1 week ago"
            ></v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
