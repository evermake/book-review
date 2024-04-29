<script setup>
defineProps({
  color: {
    type: String,
    default: 'gray'
  }
})
</script>

<template>
  <button
    class="px-3 py-1 border"
    :class="[
      (color === 'gray' && 'bg-gray bg-op-10 border-gray hover:bg-op-20'),
      (color === 'red' && 'bg-red bg-op-10 border-red hover:bg-op-20 text-red-7'),
    ]"
  >
    <slot />
  </button>
</template>
