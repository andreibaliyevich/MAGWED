<script setup>
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n({ useScope: 'global' })

const socialLinkListLoading = ref(true)
const socialLinkListUpdating = ref(false)
const socialLinkList = ref([])

const socialLinkUuid = ref(null)
const socialLinkType = ref(null)
const socialLinkUrl = ref('')

const linkTypeOptions = ref([])

const errors = ref(null)

const organizerLinkModal = ref(null)
const organizerLinkModalBootstrap = ref(null)

const setLinkTypeOptions = () => {
  linkTypeOptions.value = [
    { value: 1, text: t('auth.sociallinks.facebook') },
    { value: 2, text: t('auth.sociallinks.twitter') },
    { value: 3, text: t('auth.sociallinks.instagram') },
    { value: 4, text: t('auth.sociallinks.linkedin') },
    { value: 5, text: t('auth.sociallinks.spotify') },
    { value: 6, text: t('auth.sociallinks.youtube') },
    { value: 7, text: t('auth.sociallinks.soundcloud') },
    { value: 8, text: t('auth.sociallinks.pinterest') },
    { value: 9, text: t('auth.sociallinks.vk') }
  ]
}

const getSocialLinks = async () => {
  try {
    const response = await axios.get('/social/links/')
    socialLinkList.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    socialLinkListLoading.value = false
  }
}

const addSocialLink = async () => {
  socialLinkListUpdating.value = true
  try {
    const response = await axios.post('/social/links/', {
      link_type: socialLinkType.value,
      link_url: socialLinkUrl.value
    })
    socialLinkList.value.push(response.data)
    organizerLinkModalBootstrap.value.hide()
    errors.value = null
  } catch (error) {
    errors.value = error.response.data
  } finally {
    socialLinkListUpdating.value = false
  }
}

const updateSocialLink = async () => {
  socialLinkListUpdating.value = true
  try {
    const response = await axios.put(
      '/social/links/'
        + socialLinkUuid.value
        +'/',
      {
        link_type: socialLinkType.value,
        link_url: socialLinkUrl.value
      }
    )
    const foundIndex = socialLinkList.value.findIndex((element) => {
      return element.uuid == socialLinkUuid.value
    })
    socialLinkList.value[foundIndex] = response.data
    errors.value = null
    organizerLinkModalBootstrap.value.hide()
  } catch (error) {
    errors.value = error.response.data
  } finally {
    socialLinkListUpdating.value = false
  }
}

const removeSocialLink = async (olUuid) => {
  try {
    const response = axios.delete('/social/links/' + olUuid +'/')
    socialLinkList.value = socialLinkList.value.filter((element) => {
      return element.uuid !== olUuid
    })
  } catch (error) {
    console.error(error)
  }
}

const submitSocialLinkForm = () => {
  if (socialLinkUuid.value) {
    updateSocialLink()
  } else {
    addSocialLink()
  }
}

watch(locale, () => {
  setLinkTypeOptions()
})

onMounted(() => {
  setLinkTypeOptions()
  getSocialLinks()
  organizerLinkModal.value.addEventListener('hidden.bs.modal', () => {
    socialLinkUuid.value = null
    socialLinkType.value = null
    socialLinkUrl.value = ''
    errors.value = null
  })
  organizerLinkModalBootstrap.value = new bootstrap.Modal(
    organizerLinkModal.value
  )
})
</script>

<template>
  <div class="social-links-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('auth.sociallinks.social_links') }}
      </h1>

      <LoadingIndicator v-if="socialLinkListLoading" />
      <ul
        v-else-if="socialLinkList.length > 0"
        class="list-group list-group-flush"
      >
        <li
          v-for="socialLinkItem in socialLinkList"
          :key="socialLinkItem.uuid"
          class="list-group-item"
        >
          <div class="row">
            <div class="col-3 col-md-2">
              <span
                v-if="socialLinkItem.link_type == 1"
                class="badge bg-facebook"
              >
                {{ $t('auth.sociallinks.facebook') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 2"
                class="badge bg-twitter"
              >
                {{ $t('auth.sociallinks.twitter') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 3"
                class="badge bg-instagram"
              >
                {{ $t('auth.sociallinks.instagram') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 4"
                class="badge bg-linkedin"
              >
                {{ $t('auth.sociallinks.linkedin') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 5"
                class="badge bg-spotify"
              >
                {{ $t('auth.sociallinks.spotify') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 6"
                class="badge bg-youtube"
              >
                {{ $t('auth.sociallinks.youtube') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 7"
                class="badge bg-soundcloud"
              >
                {{ $t('auth.sociallinks.soundcloud') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 8"
                class="badge bg-pinterest"
              >
                {{ $t('auth.sociallinks.pinterest') }}
              </span>
              <span
                v-else-if="socialLinkItem.link_type == 9"
                class="badge bg-vk"
              >
                {{ $t('auth.sociallinks.vk') }}
              </span>
            </div>
            <div class="col-6 col-md-8 overflow-hidden">
              <a
                :href="socialLinkItem.link_url"
                target="_blank"
              >
                {{ socialLinkItem.link_url }}
              </a>
            </div>
            <div class="col-3 col-md-2 d-flex justify-content-end">
              <button
                @click="() => {
                  socialLinkUuid = socialLinkItem.uuid
                  socialLinkType = socialLinkItem.link_type
                  socialLinkUrl = socialLinkItem.link_url
                }"
                type="button"
                class="btn btn-light btn-sm"
                data-bs-toggle="modal"
                data-bs-target="#organizer_link_modal"
              >
                <i class="fa-solid fa-pen fa-sm"></i>
              </button>
              <button
                @click="removeSocialLink(socialLinkItem.uuid)"
                type="button"
                class="btn btn-danger btn-sm ms-1"
              >
                <i class="fa-solid fa-trash fa-sm"></i>
              </button>
            </div>
          </div>
        </li>
      </ul>
      <div
        v-else
        class="lead"
      >
        {{ $t('auth.sociallinks.do_not_have_social_links') }}
      </div>
      <button
        class="btn btn-brand mt-4"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#organizer_link_modal"
      >
        {{ $t('auth.sociallinks.add_link') }}
      </button>
    </div>
    <Teleport to="body">
      <div
        ref="organizerLinkModal"
        id="organizer_link_modal"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        aria-labelledby="organizer_link_modal_label"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                v-if="socialLinkUuid"
                id="organizer_link_modal_label"
                class="modal-title"
              >
                {{ $t('auth.sociallinks.changing_the_link') }}
              </h5>
              <h5
                v-else
                id="organizer_link_modal_label"
                class="modal-title"
              >
                {{ $t('auth.sociallinks.adding_a_link') }}
              </h5>
              <button
                class="btn-close"
                type="button"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="submitSocialLinkForm()"
                id="social_link_form"
                class="row g-3"
              >
                <div class="col-md-12">
                  <BaseSelect
                    v-model="socialLinkType"
                    :options="linkTypeOptions"
                    id="id_link_type"
                    name="link_type"
                    :label="$t('auth.sociallinks.type_of_link')"
                    :errors="errors?.link_type ? errors.link_type : []"
                  />
                </div>
                <div class="col-md-12">
                  <BaseInput
                    v-model="socialLinkUrl"
                    type="url"
                    maxlength="200"
                    id="id_link_url"
                    name="link_url"
                    :label="$t('auth.sociallinks.url_of_link')"
                    :errors="errors?.link_url ? errors.link_url : []"
                  />
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-light"
                data-bs-dismiss="modal"
              >
                {{ $t('btn.cancel') }}
              </button>
              <SubmitButton
                v-if="socialLinkUuid"
                :loadingStatus="socialLinkListUpdating"
                form="social_link_form"
                buttonClass="btn btn-brand"
                :disabled="!socialLinkType || !socialLinkUrl"
              >
                {{ $t('btn.update') }}
              </SubmitButton>
              <SubmitButton
                v-else
                :loadingStatus="socialLinkListUpdating"
                form="social_link_form"
                buttonClass="btn btn-brand"
                :disabled="!socialLinkType || !socialLinkUrl"
              >
                {{ $t('btn.add') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
