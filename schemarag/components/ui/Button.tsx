import * as React from "react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => {
    return (
      <motion.div whileTap={{ scale: 0.97 }} className="inline-block flex-shrink-0">
        <button
          className={cn(
            "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
            "bg-zinc-50 text-zinc-900 shadow hover:bg-zinc-200 h-10 px-4 py-2",
            className
          )}
          ref={ref}
          {...props}
        />
      </motion.div>
    );
  }
);
Button.displayName = "Button";

export { Button };
