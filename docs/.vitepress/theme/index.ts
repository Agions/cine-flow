import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import HomeHero from './components/HomeHero.vue'
import CompareTable from './components/CompareTable.vue'
import Workflow from './components/Workflow.vue'
import WhySection from './components/WhySection.vue'
import TechStack from './components/TechStack.vue'
import StartCards from './components/StartCards.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout: () => h(DefaultTheme.Layout, null, {}),
  enhanceApp({ app }) {
    app.component('HomeHero', HomeHero)
    app.component('CompareTable', CompareTable)
    app.component('Workflow', Workflow)
    app.component('WhySection', WhySection)
    app.component('TechStack', TechStack)
    app.component('StartCards', StartCards)
  },
}
