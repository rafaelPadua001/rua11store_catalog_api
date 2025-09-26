<template>
    <div class="my-4">
        <ins
    class="adsbygoogle"
    style="display:block"
    :data-ad-client="client"
    :data-ad-slot="slot"
    :data-ad-format="format"
    :data-full-width-responsive="responsive"
  ></ins>
    </div>
</template>

<script setup>
import { onMounted, watch } from "vue";

const props = defineProps({
    client: { type: String, required: "ca-pub-7916033089968965" },   // ID da conta (ca-pub-...)
    slot: { type: String, required: true },     // ID do bloco
    format: { type: String, default: "auto" },  // auto, rectangle, etc.
    responsive: { type: String, default: "true" }
});

const pushAds = () => {
    try {
        (adsbygoogle = window.adsbygoogle || []).push({});
    } catch (e) {
        console.error("Erro ao renderizar AdSense", e);
    }
};

onMounted(pushAds);
watch(() => props.slot, pushAds); // se mudar o slot, re-renderiza
</script>