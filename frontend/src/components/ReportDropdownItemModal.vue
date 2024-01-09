<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const props = defineProps({
  contentType: {
    type: String,
    required: true
  },
  objectUUID: {
    type: String,
    required: true
  }
})

const reportSending = ref(false)
const reportComment = ref('')
const errors = ref(null)

const sendReportModal = ref(null)
const sendReportModalBootstrap = ref(null)

const sendReport = async () => {
  reportSending.value = true
  try {
    const response = await axios.post('/support/report/', {
      content_type: props.contentType,
      object_uuid: props.objectUUID,
      comment: reportComment.value
    })
    errors.value = null
    sendReportModalBootstrap.value.hide()
  } catch (error) {
    errors.value = error.response.data
  } finally {
    reportSending.value = false
  }
}

onMounted(() => {
  sendReportModalBootstrap.value = new bootstrap.Modal(sendReportModal.value)
  sendReportModal.value.addEventListener('hidden.bs.modal', () => {
    reportComment.value = ''
  })
})
</script>

<template>
  <div class="report-dropdown-item-modal">
    <button
      type="button"
      class="dropdown-item btn btn-link"
      data-bs-toggle="modal"
      :data-bs-target="`#send_report_modal_${objectUUID}`"
    >
      <i class="fa-solid fa-flag"></i>
      {{ $t('report.report') }}
    </button>

    <Teleport to="body">
      <div
        ref="sendReportModal"
        :id="`send_report_modal_${objectUUID}`"
        class="modal fade"
        tabindex="-1"
        aria-modal="true"
        aria-hidden="true"
        :aria-labelledby="`send_report_modal_label_${objectUUID}`"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5
                :id="`send_report_modal_label_${objectUUID}`"
                class="modal-title"
              >
                {{ $t('report.new_report') }}
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="sendReport()"
                :id="`send_report_modal_form_${objectUUID}`"
              >
                <BaseTextarea
                  v-model="reportComment"
                  id="id_comment"
                  name="comment"
                  :label="$t('report.comment')"
                  :errors="errors?.comment ? errors.comment : []"
                />
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
                :loadingStatus="reportSending"
                buttonClass="btn btn-brand"
                :form="`send_report_modal_form_${objectUUID}`"
                :disabled="!reportComment"
              >
                {{ $t('btn.send') }}
              </SubmitButton>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
