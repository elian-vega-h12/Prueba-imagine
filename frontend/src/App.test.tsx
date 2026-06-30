import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, test, vi } from 'vitest';

import App from './App';

const initialClients = [
  {
    id: '11111111-1111-1111-1111-111111111111',
    name: 'Ana Perez',
    email: 'ana@example.com',
    company: 'Finanz',
    created_at: '2026-06-28T00:00:00Z',
  },
];


const initialTickets = [
  {
    id: '22222222-2222-2222-2222-222222222222',
    client_id: '11111111-1111-1111-1111-111111111111',
    title: 'Login issue',
    description: 'Cannot access the portal.',
    status: 'Pendiente',
    created_at: '2026-06-28T00:00:00Z',
  },
];

function jsonResponse(body: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(body), { status }));
}

describe('App', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  test('renders clients and tickets from the API', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(await jsonResponse(initialClients))
      .mockResolvedValueOnce(await jsonResponse(initialTickets));

    render(<App />);

    expect((await screen.findAllByText('Ana Perez')).length).toBeGreaterThan(0);
    expect(screen.getByText('Login issue')).toBeInTheDocument();
    expect(screen.getByText('Cannot access the portal.')).toBeInTheDocument();
  });

  test('creates a client through the API', async () => {
    const fetchMock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(await jsonResponse([]))
      .mockResolvedValueOnce(await jsonResponse([]))
      .mockResolvedValueOnce(
        await jsonResponse({
          id: '33333333-3333-3333-3333-333333333333',
          name: 'Luis Gomez',
          email: 'luis@example.com',
          company: 'Acme',
          created_at: '2026-06-28T00:00:00Z',
        }, 201),
      );
    const user = userEvent.setup();

    render(<App />);

    await user.type(await screen.findByLabelText('Name'), 'Luis Gomez');
    await user.type(screen.getByLabelText('Email'), 'luis@example.com');
    await user.type(screen.getByLabelText('Company'), 'Acme');
    await user.click(screen.getByRole('button', { name: /add client/i }));

    await waitFor(() => expect(screen.getByText('Client created')).toBeInTheDocument());
    expect(fetchMock).toHaveBeenLastCalledWith(
      'http://localhost:8000/clients',
      expect.objectContaining({ method: 'POST' }),
    );
    expect(screen.getAllByText('Luis Gomez').length).toBeGreaterThan(0);
  });

  test('creates a ticket and updates its status', async () => {
    const fetchMock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(await jsonResponse(initialClients))
      .mockResolvedValueOnce(await jsonResponse([]))
      .mockResolvedValueOnce(
        await jsonResponse({
          ...initialTickets[0],
          id: '44444444-4444-4444-4444-444444444444',
        }, 201),
      )
      .mockResolvedValueOnce(
        await jsonResponse({
          ...initialTickets[0],
          id: '44444444-4444-4444-4444-444444444444',
          status: 'En progreso',
        }),
      );
    const user = userEvent.setup();

    render(<App />);

    await screen.findAllByText('Ana Perez');
    await user.type(screen.getByLabelText('Title'), 'Login issue');
    await user.type(screen.getByLabelText('Description'), 'Cannot access the portal.');
    await user.click(screen.getByRole('button', { name: /create ticket/i }));

    await waitFor(() => expect(screen.getByText('Ticket created')).toBeInTheDocument());
    await user.selectOptions(screen.getByLabelText('Status for Login issue'), 'En progreso');

    await waitFor(() => expect(screen.getByText('Ticket status updated')).toBeInTheDocument());
    expect(fetchMock).toHaveBeenLastCalledWith(
      'http://localhost:8000/tickets/44444444-4444-4444-4444-444444444444/status',
      expect.objectContaining({ method: 'PATCH' }),
    );
  });
});
