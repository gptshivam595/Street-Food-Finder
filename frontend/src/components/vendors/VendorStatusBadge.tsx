import { Badge } from '@/components/ui/Badge';

interface VendorStatusBadgeProps {
  isOpen: boolean;
  openingTime?: string;
  closingTime?: string;
}

export function VendorStatusBadge({ isOpen }: VendorStatusBadgeProps) {
  return (
    <Badge tone={isOpen ? 'success' : 'danger'}>
      <span className="mr-1 text-[10px]">●</span>
      {isOpen ? 'Open Now' : 'Closed'}
    </Badge>
  );
}
