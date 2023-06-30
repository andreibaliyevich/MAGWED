<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n({ useScope: 'global' })

const props = defineProps({
  userUUID: {
    type: String,
    required: true
  }
})
const emit = defineEmits(['reviewCreated'])

const reviewSubmitting = ref(false)

const rating = ref(null)
const comment = ref('')
const ratingOptions = ref([])

const errors = ref(null)

const setRatingOptions = () => {
  ratingOptions.value = [
    { value: '5', text: t('organizers.rating_options', { n: 5 }) },
    { value: '4', text: t('organizers.rating_options', { n: 4 }) },
    { value: '3', text: t('organizers.rating_options', { n: 3 }) },
    { value: '2', text: t('organizers.rating_options', { n: 2 }) },
    { value: '1', text: t('organizers.rating_options', { n: 1 }) }
  ]
}

const sendReview = async () => {
  reviewSubmitting.value = true
  try {
    const response = await axios.post('/social/reviews/', {
      user: props.userUUID,
      rating: rating.value,
      comment: comment.value
    })
    rating.value = null
    comment.value = ''
    errors.value = null
    emit('reviewCreated', response.data)
  } catch (error) {
    errors.value = error.response.data
  } finally {
    reviewSubmitting.value = false
  }
}

watch(locale, () => {
  setRatingOptions()
})

onMounted(() => {
  setRatingOptions()
})
</script>

<template>
  <div class="write-review">
    <div class="card border border-light shadow-sm">
      <div class="card-body m-sm-3 m-md-4">
        <h5 class="card-title">{{ $t('organizers.write_review') }}</h5>
        <form
          @submit.prevent="sendReview()"
          class="row g-3 mt-3"
        >
          <div class="col-md-12">
            <BaseSelect
              v-model="rating"
              :options="ratingOptions"
              id="id_rating"
              name="rating"
              :label="$t('organizers.rating')"
              :errors="errors?.rating ? errors.rating : []"
            />
          </div>
          <div class="col-md-12">
            <BaseTextarea
              v-model="comment"
              id="id_comment"
              name="comment"
              :label="$t('organizers.comment')"
              :errors="errors?.comment ? errors.comment : []"
            />
          </div>
          <div class="col-12">
            <SubmitButton
              :loadingStatus="reviewSubmitting"
              buttonClass="btn btn-brand"
            >
              {{ $t('btn.send') }}
            </SubmitButton>
            <small
              v-if="errors?.create"
              class="text-danger"
            >
              {{ errors.create }}
            </small>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
