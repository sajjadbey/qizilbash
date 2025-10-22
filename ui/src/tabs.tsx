import DictionaryTab from './components/DictionaryTab';
import TransliteratorTab from './components/TransliteratorTab';

export type TabConfig = {
  id: string;
  label: string;
  component: React.ComponentType;
};

export const tabs: TabConfig[] = [
  {
    id: 'dictionary',
    label: 'Dictionary',
    component: DictionaryTab,
  },
  {
    id: 'transliterator',
    label: 'Transliterator',
    component: TransliteratorTab,
  }
];