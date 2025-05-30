import { describe, it, expect } from 'vitest';
import { screen } from '@testing-library/react';
import Dashboard from '../Dashboard';
import { renderWithRouter } from '../../test/utils';
import { mockStudents } from '../../test/mocks/handlers';
import { server } from '../../test/mocks/server';
import { http, HttpResponse } from 'msw';

describe('Dashboard Component', () => {
  it('renders loading state initially', () => {
    renderWithRouter(<Dashboard />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('displays student statistics after loading', async () => {
    renderWithRouter(<Dashboard />);
    
    // Wait for data to load
    await screen.findByText('Student Performance Dashboard');

    // Check if statistics are displayed
    expect(screen.getByText('Total Students')).toBeInTheDocument();
    expect(screen.getByText(mockStudents.length.toString())).toBeInTheDocument();
    
    // Check classification breakdown
    expect(screen.getByText('Distinction')).toBeInTheDocument();
    expect(screen.getByText('Merit')).toBeInTheDocument();
    
    // Check grade distribution
    const bars = screen.getAllByRole('button');
    expect(bars).toHaveLength(mockStudents.length);
  });

  it('navigates to student detail when histogram bar is clicked', async () => {
    const { user } = renderWithRouter(<Dashboard />);
    
    // Wait for data to load
    await screen.findByText('Student Performance Dashboard');
    
    // Find and click the first student's bar
    const bars = screen.getAllByRole('button');
    await user.click(bars[0]);
    
    // Check if URL changed to student detail
    expect(window.location.pathname).toBe(`/students/${mockStudents[0].student_id}`);
  });

  it('handles error state', async () => {
    // Override the default handler to simulate an error
    server.use(
      http.get('http://127.0.0.1:8000/students/', () => {
        return HttpResponse.json({ message: 'Internal Server Error' }, { status: 500 });
      })
    );
    
    renderWithRouter(<Dashboard />);
    
    // Wait for error message
    await screen.findByText(/error/i);
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
}); 