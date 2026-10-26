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
export function AmenitiesSection({ p, tab, setTab, tabs }) {
  return (
    p.sections.length > 0 && (
      <section id="amenities" className="section soft">
        <div className="shell">
          <Heading>{'Amenities & facilities'}</Heading>
          {p.amenities.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-12">
              {p.amenities.map((a, i) => (
                <div key={i}>
                  <Picture
                    src={a.image}
                    alt={a.title || `Amenity ${i + 1}`}
                    className="amenity-picture"
                  />
                  {a.title && <p className="mt-4">{a.title}</p>}
                </div>
              ))}
            </div>
          ) : (
            p.sections.map((s, i) => (
              <div
                className="richtext"
                dangerouslySetInnerHTML={{
                  __html: s.html,
                }}
                key={i}
              />
            ))
          )}
        </div>
      </section>
    )
  );
}
