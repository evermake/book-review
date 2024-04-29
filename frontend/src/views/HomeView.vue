<script setup>
import { refDebounced } from '@vueuse/core';
import { computed, ref } from 'vue'
import { useSearchBooksBooksGet } from '~/api'

const searchQuery = ref('')
const searchQueryDebounced = refDebounced(searchQuery, 350)
const searchTyping = computed(() => searchQueryDebounced.value !== searchQuery.value)
const searchOptions = computed(() => ({ query: searchQueryDebounced.value }))
const searchEnabled = computed(() => searchQueryDebounced.value.trim().length > 0)
const {
  data: books,
  isLoading: booksLoading,
  error: booksError,
} = useSearchBooksBooksGet(searchOptions, { query: { enabled: searchEnabled } })
</script>

<template>
  <div>
    <h1 class="text-center font-medium text-xl">Welcome to Book Review Platform!</h1>
    <div class="pt-4">
      <input
        v-model="searchQuery"
        type="search"
        placeholder="Search book..."
        class="w-full text-lg py-2 px-6 border outline-none focus-within:border-green"
      >
      <p v-if="booksLoading || searchTyping">Loading...</p>
      <div v-else-if="books" class="mt-2 grid gap-2 grid-cols-3">
        <RouterLink
          v-for="book in books.data"
          :key="book.id"
          :to="{ name: 'book', params: { bookId: book.id } }"
          class="border px-4 py-2 hover:border-green"
        >
          {{ book.title }}
        </RouterLink>
      </div>
      <p v-else-if="booksError" class="text-red">{{ booksError.message }}</p>
    </div>
  </div>
</template>
