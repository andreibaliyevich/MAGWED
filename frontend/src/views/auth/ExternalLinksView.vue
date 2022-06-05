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
      status: null,
      errors: null
    }
  },
  methods: {
    async getOrganizerLinkListData() {
      try {
        const response = await axios.get('/accounts/auth/links/')
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
        document.getElementById("btnClose").click()
        this.status = 'added_organizer_link'
        this.errors = null
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
    },
    getOrganizerLinkData(olId) {
      axios.get('/accounts/auth/links/' + olId +'/')
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
      axios.put('/accounts/auth/links/' + this.organizerLinkId +'/', {
        link_type: this.organizerLinkType,
        link_url: this.organizerLinkUrl
      })
      .then((response) => {
        const foundIndex = this.organizerLinkList.findIndex(item => item.id == this.organizerLinkId)
        this.organizerLinkList[foundIndex] = response.data
        document.getElementById("btnClose").click()
        this.status = 'updated_organizer_link'
        this.errors = null
      })
      .catch((error) => {
        this.status = null
        this.errors = error.response.data
      })
    },
    removeOrganizerLink(olId) {
      axios.delete('/accounts/auth/links/' + olId +'/')
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
      this.organizerLinkId = null
      this.organizerLinkType = ''
      this.organizerLinkUrl = ''
    }
  },
  mounted() {
    this.getOrganizerLinkListData()
  }
}
</script>

<template>
  <div class="organizer-links">
    <h1 class="display-6 mb-5">{{ $t('auth.externallinks.external_links') }}</h1>

    <div v-if="pageLoading" class="d-flex justify-content-center">
      <div class="spinner-grow text-dark" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else>
      <ul class="list-group list-group-flush">
        <li v-for="organizerLink in organizerLinkList" :key="organizerLink.id" class="list-group-item">
          <div class="row">
            <div class="col-3 col-md-2">
              <span v-if="organizerLink.link_type == 'WE'" class="badge bg-website">Website</span>
              <span v-if="organizerLink.link_type == 'IM'" class="badge bg-instagram">Instagram</span>
              <span v-if="organizerLink.link_type == 'FK'" class="badge bg-facebook">Facebook</span>
              <span v-if="organizerLink.link_type == 'TR'" class="badge bg-twitter">Twitter</span>
              <span v-if="organizerLink.link_type == 'PT'" class="badge bg-pinterest">Pinterest</span>
              <span v-if="organizerLink.link_type == 'VK'" class="badge bg-vk">VK</span>
            </div>
            <div class="col-6 col-md-8 overflow-hidden">
              <a :href="organizerLink.link_url" target="_blank">{{ organizerLink.link_url }}</a>
            </div>
            <div class="col-3 col-md-2 d-flex justify-content-end">
              <button @click="getOrganizerLinkData(organizerLink.id)" type="button" class="btn btn-light btn-sm" data-bs-toggle="modal" data-bs-target="#organizerLinkModal"><i class="fa-solid fa-pen fa-sm"></i></button>
              <button @click="removeOrganizerLink(organizerLink.id)" type="button" class="btn btn-danger btn-sm ms-1"><i class="fa-solid fa-trash fa-sm"></i></button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <div class="mt-4">
      <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#organizerLinkModal">{{ $t('auth.externallinks.add_link') }}</button>
      <div class="modal fade" id="organizerLinkModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="organizerLinkModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 v-if="!organizerLinkId" class="modal-title" id="organizerLinkModalLabel">{{ $t('auth.externallinks.adding_a_link') }}</h5>
              <h5 v-else class="modal-title" id="organizerLinkModalLabel">{{ $t('auth.externallinks.changing_the_link') }}</h5>
              <button @click="resetOrganizerLink" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label for="id_link_type" class="col-form-label">{{ $t('auth.externallinks.type_of_link') }}:</label>
                  <div v-if="errors && errors.link_type">
                    <select v-model="organizerLinkType" class="form-select is-invalid" name="link_type" id="id_link_type">
                      <option value="" selected="">---------</option>
                      <option value="WE">Website</option>
                      <option value="IM">Instagram</option>
                      <option value="FK">Facebook</option>
                      <option value="TR">Twitter</option>
                      <option value="PT" selected="">Pinterest</option>
                      <option value="VK">VK</option>
                    </select>
                    <div v-for="error in errors.link_type" class="invalid-feedback">{{ error }}</div>
                  </div>
                  <select v-else v-model="organizerLinkType" class="form-select" name="link_type" id="id_link_type">
                    <option value="" selected="">---------</option>
                    <option value="WE">Website</option>
                    <option value="IM">Instagram</option>
                    <option value="FK">Facebook</option>
                    <option value="TR">Twitter</option>
                    <option value="PT" selected="">Pinterest</option>
                    <option value="VK">VK</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label for="id_link_url" class="col-form-label">{{ $t('auth.externallinks.url_of_link') }}:</label>
                  <div v-if="errors && errors.link_url">
                    <input v-model="organizerLinkUrl" type="url" name="link_url" class="form-control is-invalid" maxlength="200" id="id_link_url">
                    <div v-for="error in errors.link_url" class="invalid-feedback">{{ error }}</div>
                  </div>
                  <input v-else v-model="organizerLinkUrl" type="url" name="link_url" class="form-control" maxlength="200" id="id_link_url">
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button @click="resetOrganizerLink" id="btnClose" type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{ $t('auth.externallinks.close') }}</button>
              <button v-if="!organizerLinkId" @click="addOrganizerLink" type="button" class="btn btn-primary">{{ $t('auth.externallinks.add') }}</button>
              <button v-else @click="updateOrganizerLink" type="button" class="btn btn-primary">{{ $t('auth.externallinks.update') }}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
