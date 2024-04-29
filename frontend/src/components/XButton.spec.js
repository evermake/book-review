import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import XButton from './XButton.vue'

describe('XButton', () => {
  it('renders properly with gray by default', () => {
    const wrapper = mount(XButton, {
      slots: { default: 'Test button' },
    })
    expect(wrapper.text()).toContain('Test button')
    expect(wrapper.classes()).toContain('bg-gray')
  })

  it('renders properly with red', () => {
    const wrapper = mount(XButton, {
      props: { color: 'red' },
      slots: { default: 'RED BUTTON' },
    })
    expect(wrapper.text()).toContain('RED BUTTON')
    expect(wrapper.classes()).toContain('bg-red')
    expect(wrapper.classes()).not.toContain('bg-gray')
  })
})
