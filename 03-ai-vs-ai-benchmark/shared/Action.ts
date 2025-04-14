import { z } from 'zod';

export type Vector = {
    x: number;
    y: number;
};

export const ActionSchema = z.object({
    action: z.discriminatedUnion('type', [
        z.object({
            type: z.literal('move'),
            agentId: z.string(),
            timestamp: z.number().optional().default(() => Date.now()),
            delta: z.object({
                x: z.number(),
                y: z.number(),
            }),
        }),
        z.object({
            type: z.literal('attack'),
            agentId: z.string(),
            targetId: z.string(),
            timestamp: z.number().optional().default(() => Date.now()),
        }),
        z.object({
            type: z.literal('talk'),
            agentId: z.string(),
            timestamp: z.number().optional().default(() => Date.now()),
            message: z.string(),
        }),
    ])
});

export type Action = z.infer<typeof ActionSchema>;