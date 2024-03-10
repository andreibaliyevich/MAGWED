<template>
  <div class="mx-md-10 mb-10">
    <h1 class="text-h4 text-md-h3 text-center my-5">
      {{ $t('portfolio.portfolio') }}
    </h1>

    <div class="bg-grey-lighten-4 rounded-lg pa-5">
      <h2>{{ $t('portfolio.albums') }}</h2>
      <v-btn
        :to="{ name: 'PortfolioAlbumList' }"
        variant="tonal"
        color="primary"
        class="text-none"
      >
        {{ $t('portfolio.view_albums') }}
      </v-btn>
    </div>

    <div class="bg-grey-lighten-4 rounded-lg pa-5 mt-5">
      <h2>{{ $t('portfolio.photos') }}</h2>
      <v-btn
        :to="{ name: 'PortfolioPhotoList' }"
        variant="tonal"
        color="primary"
        class="text-none"
      >
        {{ $t('portfolio.view_photos') }}
      </v-btn>
    </div>
  </div>
</template>
