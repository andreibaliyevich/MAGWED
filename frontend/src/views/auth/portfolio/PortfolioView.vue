<template>
  <div class="portfolio-view">
    <div class="px-1 px-lg-3 px-xl-5">
      <h1 class="display-6 mb-5">
        {{ $t('portfolio.portfolio') }}
      </h1>

      <div class="bg-light rounded-3 p-5">
        <h2>{{ $t('portfolio.albums') }}</h2>
        <p></p>
        <LocaleRouterLink
          routeName="PortfolioAlbumList"
          class="btn btn-soft-brand"
        >
          {{ $t('portfolio.view_albums') }}
        </LocaleRouterLink>
      </div>

      <div class="bg-light rounded-3 p-5 mt-2">
        <h2>{{ $t('portfolio.photos') }}</h2>
        <p></p>
        <LocaleRouterLink
          routeName="PortfolioPhotoList"
          class="btn btn-soft-brand"
        >
          {{ $t('portfolio.view_photos') }}
        </LocaleRouterLink>
      </div>

    </div>
  </div>
</template>
