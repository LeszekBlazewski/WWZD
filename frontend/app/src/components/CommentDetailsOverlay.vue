<template>
  <n-alert
    :class="alertClass"
    :style="{ backgroundColor: 'rgba(24, 24, 28, 0.95)' }"
    type="default"
    :show-icon="false"
  >
    <b>{{ warning }}</b>
    {{ limitedContent }}
  </n-alert>
</template>

<script lang="ts" setup>
  import { computed } from 'vue'
  import { NAlert } from 'naive-ui'

  interface Props {
    content: string
  }

  const props = withDefaults(defineProps<Props>(), {
    content: '',
  })

  const warning = computed(() => {
    return props.content.length <= 300
      ? ''
      : '(click on the node to view full content)\n'
  })

  const limitedContent = computed(() => {
    if (props.content.length <= 300) {
      return props.content
    }
    const shortened = props.content.substring(0, 300)
    return `${shortened}[…]`
  })

  const alertClass = computed(() => {
    return {
      hidden: props.content === '',
    }
  })
</script>

<style lang="scss" scoped>
  .n-alert {
    position: fixed;
    bottom: 45px;
    left: 15px;
    max-width: 25%;
    max-height: 33%;
    text-align: justify;
    overflow: hidden;
    word-break: break-word;
    white-space: pre-line;
  }

  .hidden {
    display: none;
  }
</style>
