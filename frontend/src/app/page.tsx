import { redirect } from 'next/navigation';

export default function Home({ searchParams }: { searchParams: { arxiv?: string } }) {
  if (searchParams.arxiv) {
    // Preserve classic URLs
    return <div>Redirecting to classic view... (Mock)</div>;
  }

  redirect('/modular_studio');
}
