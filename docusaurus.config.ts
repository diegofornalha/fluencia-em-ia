import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Fluência em IA',
  tagline: 'Domine a Inteligência Artificial com conteúdo prático e direto',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://your-library-docs.vercel.app',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For Vercel deployment, use '/'
  baseUrl: '/',

  // GitHub pages deployment config (if needed)
  organizationName: 'diegofornalha', // Usually your GitHub org/user name.
  projectName: 'docs', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Internationalization config
  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Edit URL for your repository
          editUrl: 'https://github.com/diegofornalha/docs/tree/main/docs/',

          // Show last update author and time (disabled until git is initialized)
          showLastUpdateAuthor: false,
          showLastUpdateTime: false,
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl: 'https://github.com/diegofornalha/docs/tree/main/blog/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // SEO metadata
    image: 'img/docusaurus-social-card.jpg',
    metadata: [
      {name: 'keywords', content: 'javascript, library, documentation'},
      {name: 'description', content: 'Comprehensive documentation for My JavaScript Library'},
    ],

    colorMode: {
      respectPrefersColorScheme: true,
    },

    // NAVBAR CONFIGURATION
    navbar: {
      title: 'Fluência em IA',
      logo: {
        alt: 'Fluência em IA Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/diegofornalha',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    // FOOTER CONFIGURATION
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentação',
          items: [
            {
              label: 'Começando',
              to: '/docs/comecando/visao-geral',
            },
            {
              label: 'Loop Delegação-Diligência',
              to: '/docs/comecando/licao1-video2',
            },
            {
              label: 'Loop Descrição-Discernimento',
              to: '/docs/comecando/licao1-video3',
            },
            {
              label: 'Avaliando Fluência em IA',
              to: '/docs/avaliacao/como-avaliar-os-4ds',
            },
          ],
        },
        {
          title: 'Comunidade',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/your-library',
            },
            {
              label: 'Discord',
              href: 'https://discord.gg/your-library',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/your-library',
            },
          ],
        },
        {
          title: 'Mais',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/diegofornalha',
            },
            {
              label: 'npm',
              href: 'https://www.npmjs.com/package/your-library',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Fluência em IA. Criado com Docusaurus.`,
    },

    // PRISM SYNTAX HIGHLIGHTING
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json', 'typescript', 'jsx', 'tsx'],
    },

    // ANNOUNCEMENT BAR (optional)
    // announcementBar: {
    //   id: 'support_us',
    //   content:
    //     'We are looking for contributors! If you are interested, please check out our <a target="_blank" rel="noopener noreferrer" href="#">GitHub</a>',
    //   backgroundColor: '#fafbfc',
    //   textColor: '#091E42',
    //   isCloseable: true,
    // },
  } satisfies Preset.ThemeConfig,
};

export default config;
