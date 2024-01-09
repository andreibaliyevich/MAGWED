<script setup>
import axios from 'axios'
import { useI18n } from 'vue-i18n'
import { ref, watch, onMounted } from 'vue'

const { t, locale } = useI18n({ useScope: 'global' })

const loadingStatus = ref(false)

const subject = ref(null)
const email = ref('')
const comment = ref('')

const subjectOptions = ref([])

const status = ref(null)
const errors = ref(null)

const setSubjectOptions = () => {
  subjectOptions.value = [
    { value: 1, text: t('feedback.subject_options.1') },
    { value: 2, text: t('feedback.subject_options.2') },
    { value: 3, text: t('feedback.subject_options.3') },
    { value: 4, text: t('feedback.subject_options.4') },
    { value: 5, text: t('feedback.subject_options.5') }
  ]
}

const sendFeedback = async () => {
  loadingStatus.value = true

  try {
    const response = await axios.post('/support/feedback/', {
      subject: subject.value,
      email: email.value,
      comment: comment.value
    })
    if (response.status === 201) {
      subject.value = null
      email.value = ''
      comment.value = ''
      status.value = 201
      errors.value = null
    }
  } catch (error) {
    status.value = null
    errors.value = error.response.data
  } finally {
    loadingStatus.value = false
  }
}

watch(locale, () => {
  setSubjectOptions()
})

onMounted(() => {
  setSubjectOptions()
})
</script>

<template>
  <div class="feedback-view">
    <div class="container my-5">
      <h1 class="display-6 text-center mb-5">
        {{ $t('feedback.feedback') }}
      </h1>

      <div class="row justify-content-center align-items-center">
        <div class="col-11 col-sm-10 col-md-8 col-lg-6 col-xl-5 col-xxl-4">
          <p class="lead fs-6">
            {{ $t('feedback.message1') }}
          </p>

          <div
            v-if="status === 201"
            class="alert alert-success alert-dismissible fade show"
            role="alert"
          >
            <i class="fa-solid fa-circle-check"></i>
            <span class="lead fs-6 ms-2">
              {{ $t('feedback.status201') }}
            </span>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="alert"
              aria-label="Close"
            ></button>
          </div>

          <form @submit.prevent="sendFeedback()">
            <div class="row g-3 mb-3">
              <div class="col-md-12">
                <BaseSelect
                  v-model="subject"
                  :options="subjectOptions"
                  id="id_subject"
                  name="subject"
                  :label="$t('feedback.subject')"
                  :errors="errors?.subject ? errors.subject : []"
                />
              </div>
              <div class="col-md-12">
                <BaseInput
                  v-model="email"
                  type="email"
                  maxlength="254"
                  id="id_email"
                  name="email"
                  :label="$t('feedback.email')"
                  :errors="errors?.email ? errors.email : []"
                />
              </div>
              <div class="col-md-12">
                <BaseTextarea
                  v-model="comment"
                  id="id_comment"
                  name="comment"
                  :label="$t('feedback.comment')"
                  :errors="errors?.comment ? errors.comment : []"
                />
              </div>
            </div>
            <SubmitButton
              :loadingStatus="loadingStatus"
              buttonClass="btn btn-brand btn-lg w-100"
            >
              {{ $t('btn.send') }}
            </SubmitButton>
          </form>
          <div class="small text-muted mt-2">
            {{ $t('feedback.message2') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
