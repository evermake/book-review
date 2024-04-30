<script setup>
import { useQueryClient } from '@tanstack/vue-query'
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getGetBookBooksIdGetQueryKey, useCreateOrUpdateReviewReviewsPost, useFindReviewsReviewsGet, useGetAuthorAuthorsIdGet, useGetBookBooksIdGet } from '~/api'
import XButton from '~/components/XButton.vue'
import { useAuthStore } from '~/stores/auth'

const queryClient = useQueryClient()
const route = useRoute()
const bookId = route.params.bookId
const {
  refetch,
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

const authStore = useAuthStore()
const { authorized, loading: authorizedLoading, me } = storeToRefs(authStore)
const submitReview = useCreateOrUpdateReviewReviewsPost()

const {
  data: reviews,
  isLoading: reviewsLoading,
} = useFindReviewsReviewsGet({ book_id: bookId })

function getCoverUrl(id) {
  return `${import.meta.env.VITE_API_BASE_URL}/covers/${id}?size=L`
}

const reviewComment = ref('')
const reviewRating = ref(10)

function handleReviewSubmit() {
  submitReview.mutate({
    data: {
      book_id: bookId,
      commentary: reviewComment.value,
      rating: reviewRating.value,
    },
  }, {
    onSuccess: () => {
      alert("Review added!")
      queryClient.invalidateQueries({
        queryKey: getGetBookBooksIdGetQueryKey(bookId),
      })
      refetch()
    },
  })
}
</script>

<template>
  <div>
    <p v-if="bookLoading">Loading...</p>
    <div v-else-if="book" class="grid gap-8 cols-3">
      <div class="w-full col-span-1 min-h-[400px] bg-neutral-3 rounded-lg overflow-hidden self-start shadow-dark shadow-lg">
        <img
          v-if="coverId"
          class="w-full h-auto"
          :src="getCoverUrl(coverId)"
          :alt="book.data.title"
        >
      </div>
      <div class="col-span-2">
        <h1 class="font-semibold text-2xl mb-2">{{ book.data.title }}</h1>
        <p class="mb-2 opacity-60">Author:
          <span v-if="author">{{ author.data.name }}</span>
          <span v-else-if="authorLoading">Loading...</span>
        </p>
        <p>{{ book.data.description }}</p>
        <hr class="my-2">
        <section>
          <h2 class="font-medium text-lg mb-2">Reviews</h2>
          <form
            v-if="!authorizedLoading && authorized"
            class="flex flex-col gap-2"
            @submit.prevent="handleReviewSubmit"
          > 
            <div class="flex gap-4 ">
              <h3 class="text-center text-md font-500">Leave your review:</h3>
              <span>{{ (reviewRating / 2).toFixed(1) }}</span>
              <input v-model="reviewRating" type="range" :min="2" :max="10" :step="1">
            </div>
            <textarea v-model="reviewComment" name="comment" rows="10" class="w-full border p-2"></textarea>
            <XButton type="submit">Submit</XButton>
          </form>
          <RouterLink
            v-else-if="!authorLoading && !authorized"
            :to="{ name: 'login', params: { redirect: route.fullPath } }"
          >
            <XButton>Login to write a review</XButton>
          </RouterLink>
          <hr class="my-4" />
          <p v-if="reviewsLoading">Loading...</p>
          <p v-else-if="reviews && reviews.data.length === 0" class="opacity-60">No reviews yet</p>
          <div v-else-if="reviews" class="flex flex-col gap-4">
            <div v-for="review in reviews.data" class="border p-4 relative" :key="review.user_id">
              <span v-if="review.user_id === me.id" class="absolute right-6 top-4 text-sm text-green-8 opacity-80 font-bold italic">Your review</span>
              <p class="font-italic">Rating: {{ (review.rating / 2).toFixed(1) }} / 5.0</p>
              <p class="pt-2">{{ review.commentary }}</p>
            </div>
          </div>
        </section>
      </div>
    </div>
    <p v-else-if="bookError" class="text-red">{{ bookError.message }}</p>
  </div>
</template>
