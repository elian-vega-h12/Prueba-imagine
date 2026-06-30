export type TicketStatus = 'Pendiente' | 'En progreso' | 'Finalizado';

export type Client = {
  id: string;
  name: string;
  email: string;
  company: string;
  created_at: string;
};

export type Ticket = {
  id: string;
  client_id: string;
  title: string;
  description: string;
  status: TicketStatus;
  created_at: string;
};


export type ClientCreate = Pick<Client, 'name' | 'email' | 'company'>;

export type TicketCreate = {
  client_id: string;
  title: string;
  description: string;
};

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const { headers, ...rest } = options ?? {};
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(headers ?? {}),
    },
    ...rest,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: response.statusText }));
    let message = 'Request failed';
    if (typeof body.detail === 'string') {
      message = body.detail;
    } else if (Array.isArray(body.detail)) {
      message = body.detail.map((err: any) => `${err.loc?.slice(1).join('.') || 'field'}: ${err.msg}`).join(', ');
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export function listClients(): Promise<Client[]> {
  return request<Client[]>('/clients');
}

export function createClient(payload: ClientCreate): Promise<Client> {
  return request<Client>('/clients', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function listTickets(): Promise<Ticket[]> {
  return request<Ticket[]>('/tickets');
}

export function createTicket(payload: TicketCreate): Promise<Ticket> {
  return request<Ticket>('/tickets', {
    method: 'POST',
    body: JSON.stringify(payload),
    headers: { 'X-User': 'frontend' },
  });
}

export function updateTicketStatus(ticketId: string, status: TicketStatus): Promise<Ticket> {
  return request<Ticket>(`/tickets/${ticketId}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
    headers: { 'X-User': 'frontend' },
  });
}
