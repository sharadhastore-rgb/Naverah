import { useState } from 'react';
import {
  ArrowDown,
  ArrowUpRight,
  Building2,
  Check,
  HeartHandshake,
  Lightbulb,
  Mail,
  MapPin,
  Phone,
  Search,
  ShieldCheck,
  Users,
} from 'lucide-react';
import { articles, contact, data, properties, services } from '../../../data.js';
import {
  BlogCard,
  Button,
  ContactForm,
  CTA,
  FAQ,
  Gallery,
  Heading,
  Office,
  Pagination,
  Picture,
  PropertyCard,
  ServiceGrid,
  TeamGrid,
} from '../../../components/index.js';
export function TeamSection() {
  return (
    <section className="section">
      <div className="shell">
        <div className="section-head reveal">
          <Heading>
            {'The people behind'}
            <br />
            {'Naverah Assets'}
          </Heading>
          <Button href="/agent" outline arrow={false}>
            {'Meet our team'}
          </Button>
        </div>
        <TeamGrid />
      </div>
    </section>
  );
}
