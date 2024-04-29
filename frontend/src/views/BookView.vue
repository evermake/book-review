<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useGetBookBooksIdGet } from '~/api';

const bookId = useRoute().params.bookId
const {
  data: book,
  isLoading: bookLoading,
  error: bookError,
} = useGetBookBooksIdGet(bookId)
const coverId = computed(() => book.value?.data.covers?.[0] ?? null)

function getCoverUrl(id) {
  return `${import.meta.env.VITE_API_BASE_URL}/covers/${id}?size=L`
}
</script>

<template>
  <div>
    <p v-if="bookLoading">Loading...</p>
    <div v-else-if="book" class="grid gap-8 cols-3">
      <div class="w-full col-span-1 min-h-[400px] bg-neutral-3 rounded-lg overflow-hidden">
        <img
          v-if="coverId"
          class="w-full h-auto"
          :src="getCoverUrl(coverId)"
          :alt="book.data.title"
        >
      </div>  
      <div class="col-span-2">
        <h1 class="font-semibold text-2xl mb-2">{{ book.data.title }}</h1>
        <p>{{ book.data.description }}</p>
        <hr class="my-2">
        <section>
          <h2 class="font-medium text-lg">Reviews</h2>
        </section>
      </div>
    </div>
    <p v-else-if="bookError" class="text-red">{{ bookError.message }}</p>
  </div>
</template>
