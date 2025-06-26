// Custom JavaScript for AgentTest documentation

document.addEventListener('DOMContentLoaded', function () {
  // Add copy buttons to code blocks
  addCopyButtons()

  // Add version badges to new features
  addVersionBadges()

  // Enhance API documentation
  enhanceApiDocs()

  // Add example toggles
  addExampleToggles()
})

function addCopyButtons() {
  // Add copy buttons to code blocks that don't already have them
  const codeBlocks = document.querySelectorAll('pre > code')

  codeBlocks.forEach((codeBlock) => {
    const pre = codeBlock.parentNode

    // Skip if copy button already exists
    if (pre.querySelector('.copy-button')) return

    const copyButton = document.createElement('button')
    copyButton.className = 'copy-button'
    copyButton.innerHTML = '📋'
    copyButton.title = 'Copy to clipboard'

    copyButton.addEventListener('click', () => {
      const text = codeBlock.textContent
      navigator.clipboard.writeText(text).then(() => {
        copyButton.innerHTML = '✅'
        setTimeout(() => {
          copyButton.innerHTML = '📋'
        }, 2000)
      })
    })

    pre.style.position = 'relative'
    copyButton.style.position = 'absolute'
    copyButton.style.top = '0.5rem'
    copyButton.style.right = '0.5rem'
    copyButton.style.border = 'none'
    copyButton.style.background = 'rgba(0, 0, 0, 0.1)'
    copyButton.style.borderRadius = '0.25rem'
    copyButton.style.padding = '0.25rem'
    copyButton.style.cursor = 'pointer'

    pre.appendChild(copyButton)
  })
}

function addVersionBadges() {
  // Add version badges to new features
  const newFeatures = document.querySelectorAll('[data-version]')

  newFeatures.forEach((element) => {
    const version = element.getAttribute('data-version')
    const badge = document.createElement('span')
    badge.className = 'version-badge'
    badge.textContent = `v${version}`

    // Insert badge after the element's title or first text node
    const title = element.querySelector('h1, h2, h3, h4, h5, h6')
    if (title) {
      title.appendChild(badge)
    }
  })
}

function enhanceApiDocs() {
  // Add interactive features to API documentation
  const apiMethods = document.querySelectorAll('.api-method')

  apiMethods.forEach((method) => {
    method.addEventListener('click', () => {
      // Highlight the method when clicked
      method.style.backgroundColor = 'var(--md-primary-fg-color)'
      method.style.color = 'white'

      setTimeout(() => {
        method.style.backgroundColor = ''
        method.style.color = ''
      }, 1000)
    })
  })

  // Add parameter highlighting
  const parameters = document.querySelectorAll('.api-parameter')

  parameters.forEach((param) => {
    param.addEventListener('mouseenter', () => {
      param.style.backgroundColor = 'var(--md-primary-fg-color)'
      param.style.color = 'white'
    })

    param.addEventListener('mouseleave', () => {
      param.style.backgroundColor = ''
      param.style.color = ''
    })
  })
}

function addExampleToggles() {
  // Add toggle functionality to example blocks
  const examples = document.querySelectorAll('.example-block')

  examples.forEach((example) => {
    const title = example.querySelector('.example-title')
    const content = example.querySelector('.example-content')

    if (title && content) {
      title.style.cursor = 'pointer'
      title.innerHTML += ' <span style="float: right;">▼</span>'

      title.addEventListener('click', () => {
        const isHidden = content.style.display === 'none'
        content.style.display = isHidden ? 'block' : 'none'

        const arrow = title.querySelector('span')
        arrow.textContent = isHidden ? '▼' : '▶'
      })
    }
  })
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute('href'))
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      })
    }
  })
})

// Add search result highlighting
function highlightSearchResults() {
  const urlParams = new URLSearchParams(window.location.search)
  const query = urlParams.get('q')

  if (query) {
    const content = document.querySelector('.md-content')
    if (content) {
      const walker = document.createTreeWalker(
        content,
        NodeFilter.SHOW_TEXT,
        null,
        false
      )

      const textNodes = []
      let node

      while ((node = walker.nextNode())) {
        textNodes.push(node)
      }

      textNodes.forEach((textNode) => {
        const parent = textNode.parentNode
        if (parent.tagName !== 'SCRIPT' && parent.tagName !== 'STYLE') {
          const regex = new RegExp(`(${query})`, 'gi')
          const newHTML = textNode.textContent.replace(regex, '<mark>$1</mark>')

          if (newHTML !== textNode.textContent) {
            const wrapper = document.createElement('span')
            wrapper.innerHTML = newHTML
            parent.replaceChild(wrapper, textNode)
          }
        }
      })
    }
  }
}

// Initialize search highlighting after page load
window.addEventListener('load', highlightSearchResults)
