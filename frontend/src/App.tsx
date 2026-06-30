import { Plus, RefreshCw, Save } from 'lucide-react';
import { FormEvent, useEffect, useMemo, useState } from 'react';

import {
  Client,
  Ticket,
  TicketStatus,
  createClient,
  createTicket,
  listClients,
  listTickets,
  updateTicketStatus,
} from './api';

const ticketStatuses: TicketStatus[] = ['Pendiente', 'En progreso', 'Finalizado'];


type LoadState = 'idle' | 'loading' | 'ready' | 'error';

function App() {
  const [clients, setClients] = useState<Client[]>([]);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loadState, setLoadState] = useState<LoadState>('idle');
  const [message, setMessage] = useState<string>('');

  const [clientForm, setClientForm] = useState({ name: '', email: '', company: '' });
  const [ticketForm, setTicketForm] = useState({ client_id: '', title: '', description: '' });

  const clientById = useMemo(
    () => new Map(clients.map((client) => [client.id, client])),
    [clients],
  );

  async function loadData() {
    setLoadState('loading');
    setMessage('');
    try {
      const [loadedClients, loadedTickets] = await Promise.all([listClients(), listTickets()]);
      setClients(loadedClients);
      setTickets(loadedTickets);
      setTicketForm((current) => ({
        ...current,
        client_id: current.client_id || loadedClients[0]?.id || '',
      }));
      setLoadState('ready');
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Could not load data');
      setLoadState('error');
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  async function handleCreateClient(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage('');
    try {
      const created = await createClient(clientForm);
      setClients((current) => [...current, created]);
      setTicketForm((current) => ({ ...current, client_id: current.client_id || created.id }));
      setClientForm({ name: '', email: '', company: '' });
      setMessage('Client created');
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Could not create client');
    }
  }

  async function handleCreateTicket(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage('');
    try {
      const created = await createTicket(ticketForm);
      setTickets((current) => [...current, created]);
      setTicketForm((current) => ({ ...current, title: '', description: '' }));
      setMessage('Ticket created');
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Could not create ticket');
    }
  }

  async function handleStatusChange(ticketId: string, status: TicketStatus) {
    setMessage('');
    try {
      const updated = await updateTicketStatus(ticketId, status);
      setTickets((current) =>
        current.map((ticket) => (ticket.id === ticketId ? updated : ticket)),
      );
      setMessage('Ticket status updated');
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Could not update ticket');
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Support desk</p>
          <h1>Customer tickets</h1>
        </div>
        <button className="icon-button" type="button" onClick={() => void loadData()} aria-label="Refresh data">
          <RefreshCw size={18} />
        </button>
      </header>

      {message ? <div className="notice">{message}</div> : null}
      {loadState === 'loading' ? <div className="notice">Loading data...</div> : null}
      {loadState === 'error' ? <div className="notice error">Backend is not reachable.</div> : null}

      <section className="workspace">
        <div className="panel">
          <div className="panel-heading">
            <h2>Clients</h2>
            <span>{clients.length}</span>
          </div>

          <form className="form" onSubmit={(event) => void handleCreateClient(event)}>
            <label>
              Name
              <input
                required
                value={clientForm.name}
                onChange={(event) => setClientForm({ ...clientForm, name: event.target.value })}
              />
            </label>
            <label>
              Email
              <input
                required
                type="email"
                value={clientForm.email}
                onChange={(event) => setClientForm({ ...clientForm, email: event.target.value })}
              />
            </label>
            <label>
              Company
              <input
                required
                value={clientForm.company}
                onChange={(event) => setClientForm({ ...clientForm, company: event.target.value })}
              />
            </label>
            <button type="submit">
              <Plus size={16} />
              Add client
            </button>
          </form>

          <div className="list">
            {clients.length === 0 && loadState === 'ready' ? (
              <p className="empty">No clients yet.</p>
            ) : null}
            {clients.map((client) => (
              <article className="row" key={client.id}>
                <div>
                  <strong>{client.name}</strong>
                  <p>{client.email}</p>
                </div>
                <span>{client.company}</span>
              </article>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-heading">
            <h2>Tickets</h2>
            <span>{tickets.length}</span>
          </div>

          <form className="form" onSubmit={(event) => void handleCreateTicket(event)}>
            <label>
              Client
              <select
                required
                value={ticketForm.client_id}
                onChange={(event) => setTicketForm({ ...ticketForm, client_id: event.target.value })}
              >
                <option value="" disabled>
                  Select a client
                </option>
                {clients.map((client) => (
                  <option key={client.id} value={client.id}>
                    {client.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Title
              <input
                required
                value={ticketForm.title}
                onChange={(event) => setTicketForm({ ...ticketForm, title: event.target.value })}
              />
            </label>
            <label>
              Description
              <textarea
                required
                rows={3}
                value={ticketForm.description}
                onChange={(event) =>
                  setTicketForm({ ...ticketForm, description: event.target.value })
                }
              />
            </label>
            <button type="submit" disabled={clients.length === 0}>
              <Save size={16} />
              Create ticket
            </button>
          </form>

          <div className="list">
            {tickets.length === 0 && loadState === 'ready' ? (
              <p className="empty">No tickets yet.</p>
            ) : null}
            {tickets.map((ticket) => (
              <article className="row ticket-row" key={ticket.id}>
                <div>
                  <strong>{ticket.title}</strong>
                  <p>{ticket.description}</p>
                  <small>{clientById.get(ticket.client_id)?.name ?? 'Unknown client'}</small>
                </div>
                <select
                  aria-label={`Status for ${ticket.title}`}
                  value={ticket.status}
                  onChange={(event) =>
                    void handleStatusChange(ticket.id, event.target.value as TicketStatus)
                  }
                >
                  {ticketStatuses.map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

export default App;
