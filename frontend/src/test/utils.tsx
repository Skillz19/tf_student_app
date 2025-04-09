import { ReactElement } from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import userEvent from '@testing-library/user-event';

export function renderWithRouter(ui: ReactElement) {
  return {
    user: userEvent.setup(),
    ...render(ui, {
      wrapper: BrowserRouter
    })
  };
} 