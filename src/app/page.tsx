import V2Site from "@/components/v2-site";
import { V2_DESCRIPTION, V2_TITLE } from "@/components/v2-body.generated";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: { absolute: V2_TITLE },
  description: V2_DESCRIPTION,
};

export default function Home() {
  return <V2Site />;
}
