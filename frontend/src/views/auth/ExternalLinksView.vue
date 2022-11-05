<script setup>
import axios from 'axios'
</script>

<script>
export default {
  data() {
    return {
      pageLoading: true,
      organizerLinkList: [],
      organizerLinkId: null,
      organizerLinkType: '',
      organizerLinkUrl: '',
      linkTypeOptions: [
        { value: 'WE', text: 'Website' },
        { value: 'FK', text: 'Facebook' },
        { value: 'TR', text: 'Twitter' },
        { value: 'IM', text: 'Instagram' },
        { value: 'SY', text: 'Spotify' },
        { value: 'YE', text: 'YouTube' },
        { value: 'SD', text: 'SoundCloud' },
        { value: 'PT', text: 'Pinterest' },
        { value: 'VK', text: 'VK' },
        { value: 'LN', text: 'LinkedIn' }
      ],
      status: null,
      errors: null
    }
  },
  methods: {
    async getOrganizerLinkListData() {
      try {
        const response = await axios.get('/' + this.$i18n.locale + '/accounts/auth/links/')
        this.organizerLinkList = response.data
      } catch (error) {
        this.errors = error.response.data
      } finally {
        this.pageLoading = false
      }
    },
    addOrganizerLink() {
      axios.post('/' + this.$i18n.locale + '/accounts/auth/links/', {
        link_type: this.organizerLinkType,
        link_url: this.organizerLinkUrl
      })
      .then((response) => {
        this.organizerLinkList.push(response.data)
        this.$refs.btnClose.click()
        this.status = 'added_organizer_link'
        this.errors = null
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
    },
    getOrganizerLinkData(olId) {
      axios.get('/' + this.$i18n.locale + '/accounts/auth/links/' + olId +'/')
      .then((response) => {
        this.organizerLinkId = response.data.id
        this.organizerLinkType = response.data.link_type
        this.organizerLinkUrl = response.data.link_url
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
    },
    updateOrganizerLink() {
      axios.put('/' + this.$i18n.locale + '/accounts/auth/links/' + this.organizerLinkId +'/', {
        link_type: this.organizerLinkType,
        link_url: this.organizerLinkUrl
      })
      .then((response) => {
        const foundIndex = this.organizerLinkList.findIndex(item => item.id == this.organizerLinkId)
        this.organizerLinkList[foundIndex] = response.data
        this.$refs.btnClose.click()
        this.status = 'updated_organizer_link'
        this.errors = null
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
    },
    removeOrganizerLink(olId) {
      axios.delete('/' + this.$i18n.locale + '/accounts/auth/links/' + olId +'/')
      .then((response) => {
        const foundIndex = this.organizerLinkList.findIndex(item => item.id == olId)
        this.organizerLinkList.splice(foundIndex, 1)
        this.status = 'removed_organizer_link'
        this.errors = null
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
    },
    resetOrganizerLink() {
      setTimeout(() => {
        this.organizerLinkId = null
        this.organizerLinkType = ''
        this.organizerLinkUrl = ''
      }, 500)
    }
  },
  mounted() {
    this.getOrganizerLinkListData()
  }
}
</script>

<template>
  <div class="organizer-links px-1 px-lg-3 px-xl-5">
    <h1 class="display-6 mb-5">
      {{ $t('auth.externallinks.external_links') }}
    </h1>

    <div
      v-if="pageLoading"
      class="d-flex justify-content-center"
    >
      <div
        class="spinner-grow text-dark"
        role="status"
      >
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else>
      <ul class="list-group list-group-flush">
        <li
          v-for="organizerLink in organizerLinkList"
          :key="organizerLink.id"
          class="list-group-item"
        >
          <div class="row">
            <div class="col-3 col-md-2">
              <span
                v-if="organizerLink.link_type == 'WE'"
                class="badge bg-website"
              >
                Website
              </span>
              <span
                v-else-if="organizerLink.link_type == 'FK'"
                class="badge bg-facebook"
              >
                Facebook
              </span>
              <span
                v-else-if="organizerLink.link_type == 'TR'"
                class="badge bg-twitter"
              >
                Twitter
              </span>
              <span
                v-else-if="organizerLink.link_type == 'IM'"
                class="badge bg-instagram"
              >
                Instagram
              </span>
              <span
                v-else-if="organizerLink.link_type == 'SY'"
                class="badge bg-spotify"
              >
                Spotify
              </span>
              <span
                v-else-if="organizerLink.link_type == 'YE'"
                class="badge bg-youtube"
              >
                YouTube
              </span>
              <span
                v-else-if="organizerLink.link_type == 'SD'"
                class="badge bg-soundcloud"
              >
                SoundCloud
              </span>
              <span
                v-else-if="organizerLink.link_type == 'PT'"
                class="badge bg-pinterest"
              >
                Pinterest
              </span>
              <span
                v-else-if="organizerLink.link_type == 'VK'"
                class="badge bg-vk"
              >
                VK
              </span>
              <span
                v-else-if="organizerLink.link_type == 'LN'"
                class="badge bg-linkedin"
              >
                LinkedIn
              </span>
            </div>
            <div class="col-6 col-md-8 overflow-hidden">
              <a
                :href="organizerLink.link_url"
                target="_blank"
              >
                {{ organizerLink.link_url }}
              </a>
            </div>
            <div class="col-3 col-md-2 d-flex justify-content-end">
              <button
                @click="getOrganizerLinkData(organizerLink.id)"
                type="button"
                class="btn btn-light btn-sm"
                data-bs-toggle="modal"
                data-bs-target="#organizerLinkModal"
              >
                <i class="fa-solid fa-pen fa-sm"></i>
              </button>
              <button
                @click="removeOrganizerLink(organizerLink.id)"
                type="button"
                class="btn btn-danger btn-sm ms-1"
              >
                <i class="fa-solid fa-trash fa-sm"></i>
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <div class="mt-4">
      <button
        type="button"
        class="btn btn-brand"
        data-bs-toggle="modal"
        data-bs-target="#organizerLinkModal"
      >
        {{ $t('auth.externallinks.add_link') }}
      </button>
      <div
        class="modal fade"
        id="organizerLinkModal"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabindex="-1"
        aria-labelledby="organizerLinkModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                v-if="!organizerLinkId"
                class="modal-title"
                id="organizerLinkModalLabel"
              >
                {{ $t('auth.externallinks.adding_a_link') }}
              </h5>
              <h5
                v-else
                class="modal-title"
                id="organizerLinkModalLabel"
              >
                {{ $t('auth.externallinks.changing_the_link') }}
              </h5>
              <button
                @click="resetOrganizerLink"
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label
                    for="id_link_type"
                    class="col-form-label"
                  >
                    {{ $t('auth.externallinks.type_of_link') }}:
                  </label>
                  <div v-if="errors && errors.link_type">
                    <select
                      v-model="organizerLinkType"
                      class="form-select is-invalid"
                      name="link_type"
                      id="id_link_type"
                    >
                      <option
                        disabled
                        value=""
                      >
                        ---------
                      </option>
                      <option
                        v-for="option in linkTypeOptions"
                        :value="option.value"
                      >
                        {{ option.text }}
                      </option>
                    </select>
                    <div
                      v-for="error in errors.link_type"
                      class="invalid-feedback"
                    >
                      {{ error }}
                    </div>
                  </div>
                  <select
                    v-else
                    v-model="organizerLinkType"
                    class="form-select"
                    name="link_type"
                    id="id_link_type"
                  >
                    <option
                      disabled
                      value=""
                    >
                      ---------
                    </option>
                    <option
                      v-for="option in linkTypeOptions"
                      :value="option.value"
                    >
                      {{ option.text }}
                    </option>
                  </select>
                </div>
                <div class="mb-3">
                  <label
                    for="id_link_url"
                    class="col-form-label"
                  >
                    {{ $t('auth.externallinks.url_of_link') }}:
                  </label>
                  <div v-if="errors && errors.link_url">
                    <input
                      v-model="organizerLinkUrl"
                      type="url"
                      name="link_url"
                      class="form-control is-invalid"
                      maxlength="200"
                      id="id_link_url"
                    >
                    <div
                      v-for="error in errors.link_url"
                      class="invalid-feedback"
                    >
                      {{ error }}
                    </div>
                  </div>
                  <input
                    v-else
                    v-model="organizerLinkUrl"
                    type="url"
                    name="link_url"
                    class="form-control"
                    maxlength="200"
                    id="id_link_url"
                  >
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                ref="btnClose"
                @click="resetOrganizerLink"
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                {{ $t('auth.externallinks.close') }}
              </button>
              <button
                v-if="!organizerLinkId"
                @click="addOrganizerLink"
                type="button"
                class="btn btn-primary"
              >
                {{ $t('auth.externallinks.add') }}
              </button>
              <button
                v-else
                @click="updateOrganizerLink"
                type="button"
                class="btn btn-primary"
              >
                {{ $t('auth.externallinks.update') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
