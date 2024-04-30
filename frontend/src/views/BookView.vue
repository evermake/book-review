<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useFindReviewsReviewsGet, useGetAuthorAuthorsIdGet, useGetBookBooksIdGet } from '~/api'

const bookId = useRoute().params.bookId
const {
  data: book,
  isLoading: bookLoading,
  error: bookError,
} = useGetBookBooksIdGet(bookId)
const coverId = computed(() => book.value?.data.covers?.[0] ?? null)
const authorId = computed(() => book.value?.data?.author_id)
const authorEnabled = computed(() => Boolean(authorId.value))
const {
  data: author,
  isLoading: authorLoading,
} = useGetAuthorAuthorsIdGet(authorId, { query: { enabled: authorEnabled } })

const {
  data: reviews,
  isLoading: reviewsLoading,
} = useFindReviewsReviewsGet({ book_id: bookId })

const averageRating = computed(() => reviews.value?.data.reduce((acc, r) => acc + r.rating, 0) / reviews.value?.data.length)
// const averageRating = computed(() => reviews.data)

function getCoverUrl(id) {
  return `${import.meta.env.VITE_API_BASE_URL}/covers/${id}?size=L`
}

function adjustRating(rating) {
  return (rating / 2).toFixed(1)
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
        <p class="opacity-60">
          Rating:
          <span v-if="reviewsLoading">Loading...</span>
          <span v-else-if="reviews && reviews.data.length">{{ adjustRating(averageRating) }}</span>
          <span v-else>Not rated yet</span>
        </p>
        <p class="mb-2 opacity-60">Author:
          <span v-if="author">{{ author.data.name }}</span>
          <span v-else-if="authorLoading">Loading...</span>
        </p>
        <p>{{ book.data.description }}</p>
        <hr class="my-2">
        <section>
          <h2 class="font-medium text-lg mb-2">Reviews</h2>
          <p v-if="reviewsLoading">Loading...</p>
          <p v-else-if="reviews && reviews.data.length === 0" class="opacity-60">No reviews yet</p>
          <div v-else-if="reviews" class="flex flex-col gap-4">
            <div v-for="review in reviews.data" class="border px-4 py-6">
              <p class="font-italic">Rating: {{ adjustRating(review.rating) }} / 5</p>
              <p class="pt-2">{{ review.commentary }}</p>
            </div>
          </div>
        </section>
      </div>
    </div>
    <p v-else-if="bookError" class="text-red">{{ bookError.message }}</p>
  </div>
</template>
