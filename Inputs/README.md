# Inputs information
The object of analysis is the publicly-available Hetionet biological knowledge graph, which is stored as two separate files:
- edges.sif - edge file listing information about all connections between the set of heterogeneous entities
- nodes.tsv - node file listing the unique ID, name and kind of all entities in the graph

> **References**:
>- https://het.io/about/
>- https://github.com/hetio/hetionet/tree/master/hetnet/tsv

## Edges data format
`hetionet-v1.0-edges.sif.gz` is a gzipped TSV table of network edges, formatted like:

| source                  | metaedge | target                         |
|-------------------------|----------|--------------------------------|
| Gene::9021              | GpBP     | Biological Process::GO:0071357 |
| Anatomy::UBERON:0002081 | AeG      | Gene::8519                     |
| Anatomy::UBERON:0001891 | AeG      | Gene::84281                    |
| Gene::2063              | Gr>G     | Gene::7846                     |

`source` is the source node id as in the node table

`target` is the target node id

`metaedge` is the abbreviation of the edge type

## Nodes data format
`hetionet-v1.0-nodes.tsv` is a table of network nodes, formatted like:

| id                             | name                      | kind               |
|--------------------------------|---------------------------|--------------------|
| Anatomy::UBERON:0000004        | nose                      | Anatomy            |
| Biological Process::GO:0003193 | pulmonary valve formation | Biological Process |
| Gene::3149                     | HMGB3                     | Gene               |
| Symptom::D058447               | Eye Pain                  | Symptom            |

`id` is the node identifier prepended with the node type plus '::' as a separator

`name` is the node name

`kind` is the node type